# -*- coding: utf-8 -*-
"""phoneme_verification_report.py — 学者拟音 → 音频 逐音素自动化验证报告。

用户审查要求：**「有音频输出」≠ 成功**。本脚本把整条链路拆开量化：

    原始拟音（Sinica 声母/韵母原值）
      → IPA 组合（_compose_ipa：声母+韵母，零声母记号剥离）
        → 引擎能力（language.phoneme_capability 两级矩阵：
           eSpeak-ng 主路径 / 共振峰回退，基于 2026-10-30 实测冻结集合）
          → 逐音素（token）处置：按预期合成 / 近似替代（音色丢失）/
             丢弃（该段无声）/ 未实测（不保证）

输出（默认 docs/reports/phoneme_verification/）：
- REPORT.md                    逐音素报告（快照，供人工审查）
- polyphone_verification.csv   多音字人工核验集（method + 卡因 + 空白核验列）
- polyphone_candidates.csv     多音字完整候选行（含韵部/备注/来源行号）
- summary.json                 机器可读汇总

用法:
    python scripts/phoneme_verification_report.py                # 全部 11 体系 + 旧实验字表
    python scripts/phoneme_verification_report.py --systems wangli_mc
    python scripts/phoneme_verification_report.py --out 其它目录

只读：不修改任何数据、不动引擎代码；重新生成 = 覆盖输出目录内 4 个文件。
多音字选音与线上同一代码路径（language.ancient_tts.text_to_ipa →
language.polyphone.select_reading），报告里的 empirical / fallback_first
语义与 UI 一致：empirical = 经验性选择（非学者确认），fallback_first =
不可判定时按首条回退，note 逐条写明卡因。
"""
import argparse
import csv
import json
import os
import sys
import unicodedata
from collections import OrderedDict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from language.history.sinica_scholar_data import (  # noqa: E402
    SCHOLAR_SYSTEMS_ALL, _index_by_char, load_scholar_readings)
from language.phoneme_capability import (  # noqa: E402
    ESPEAK_LEVEL_ZH, assess_ipa, system_capability_report)
from phonology_db import EASTERN_HAN_DB  # noqa: E402

#: 人工核验用的名句样本（公版古籍，逐条标注出处）。
#: 选取标准：短、常见、含多音字（行/为/说/乐/道/得/华/率/王/好/朝/中…）。
SENTENCES = [
    ("学而时习之，不亦说乎？", "论语·学而"),
    ("学而不思则罔，思而不学则殆。", "论语·为政"),
    ("三人行，必有我师焉。", "论语·述而"),
    ("温故而知新，可以为师矣。", "论语·为政"),
    ("己所不欲，勿施于人。", "论语·颜渊"),
    ("关关雎鸠，在河之洲。", "诗经·关雎"),
    ("桃之夭夭，灼灼其华。", "诗经·桃夭"),
    ("北冥有鱼，其名为鲲。", "庄子·逍遥游"),
    ("得道者多助，失道者寡助。", "孟子·公孙丑下"),
    ("大道之行也，天下为公。", "礼记·礼运"),
    ("普天之下，莫非王土。", "诗经·小雅·北山"),
    ("兼相爱，交相利。", "墨子·兼爱中"),
]

#: token 状态 → 引擎侧处置（用户审查用语：近似替代 / 丢弃 / 无法发声）
TOKEN_ZH = {
    "ok": "按预期合成",
    "approx": "近似替代（有声，重音/音色丢失）",
    "silent": "丢弃（该段无声）",
    "untested": "未实测（不保证发声）",
    "junk": "非语音 ASCII（数据质量）",
}
_SEVERITY = {"silent": 0, "untested": 1, "approx": 2, "ok": 3, "junk": 4}
_EZ = {"full": "full 全段可合成", "approx": "approx 近似",
       "partial": "partial 缺段", "untested": "untested 未实测",
       "silent": "silent 全静"}


def _nfc(s):
    return unicodedata.normalize("NFC", s)


def _esc(s):
    """markdown 表格转义。"""
    return str(s).replace("|", "\\|")


def _collect_system_tokens(readings):
    """逐读法 assess_ipa，按 token（NFC）聚合能力与例字。"""
    tokens = {}
    levels = {"full": 0, "approx": 0, "partial": 0, "untested": 0, "silent": 0}
    formant = {"full": 0, "partial": 0, "silent": 0}
    n = 0
    for rec in readings:
        if not rec.ipa:
            continue
        n += 1
        a = assess_ipa(rec.ipa)
        levels[a.espeak_level] += 1
        formant[a.formant_level] += 1
        for tc in a.tokens:
            key = _nfc(tc.token)
            slot = tokens.setdefault(key, {
                "token": key, "count": 0,
                "espeak": tc.espeak, "formant": tc.formant,
                "chars": OrderedDict(),
            })
            slot["count"] += 1
            if len(slot["chars"]) < 3:
                slot["chars"][rec.character] = (rec.initial, rec.final)
    return tokens, levels, formant, n


def _token_table(tokens):
    rows = sorted(tokens.values(),
                  key=lambda t: (_SEVERITY.get(t["espeak"], 9), -t["count"]))
    lines = ["| 音素(token) | 出现次数 | eSpeak 主路径 | 共振峰回退 | 引擎侧处置 | 例字 |",
             "|---|---:|---|---|---|---|"]
    for t in rows:
        ex = "、".join(t["chars"].keys())
        lines.append("| %s | %d | %s | %s | %s | %s |" % (
            _esc(t["token"]), t["count"], t["espeak"], t["formant"],
            TOKEN_ZH.get(t["espeak"], t["espeak"]), _esc(ex) or "—"))
    return rows, lines


def _raw_examples(readings, k=3):
    lines = []
    for rec in readings:
        if not rec.ipa:
            continue
        lines.append("| %s | %s | %s | %s |" % (
            rec.character, _esc(rec.initial) or "（零声母）",
            _esc(rec.final), _esc(rec.ipa)))
        if len(lines) >= k:
            break
    return lines


def _polyphone_chars(idx):
    """字符 → 非 suspect 且带 IPA 的行（≥2 条才算多音字）。"""
    out = {}
    for ch, recs in idx.items():
        clean = [r for r in recs if not r.suspect and r.ipa]
        if len(clean) >= 2:
            out[ch] = clean
    return out


def _run_sentence_selections(system_id):
    """跑样本句，收集多音字选音（与线上同一路径）。返回 (行, 统计)。"""
    from language.ancient_tts import text_to_ipa
    rows = {}   # (system, char, method, selected_ipa) → 行
    for text, src in SENTENCES:
        res = text_to_ipa(text, system_id=system_id)
        for ch, ipa, method, note in res.selections:
            key = (system_id, ch, method, ipa or "")
            if key not in rows:
                rows[key] = {
                    "system_id": system_id,
                    "char": ch,
                    "method": method,
                    "selected_ipa": ipa or "",
                    "note": note,
                    "occurrences": 0,
                    "example": "%s（%s）" % (text, src),
                    "tone": "",
                    "tone_class": "",
                }
            rows[key]["occurrences"] += 1
    return rows


def _legacy_tokens():
    tokens = {}
    levels = {"full": 0, "approx": 0, "partial": 0, "untested": 0, "silent": 0}
    formant = {"full": 0, "partial": 0, "silent": 0}
    chars = OrderedDict()
    for ch, data in EASTERN_HAN_DB.items():
        ipa = data.get("ipa", "")
        if not ipa:
            continue
        a = assess_ipa(ipa)
        levels[a.espeak_level] += 1
        formant[a.formant_level] += 1
        chars[ch] = ipa
        for tc in a.tokens:
            key = _nfc(tc.token)
            slot = tokens.setdefault(key, {
                "token": key, "count": 0,
                "espeak": tc.espeak, "formant": tc.formant,
                "chars": OrderedDict(),
            })
            slot["count"] += 1
            if len(slot["chars"]) < 3:
                slot["chars"][ch] = ("", "")
    return tokens, levels, formant, len(chars)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out",
                    default=os.path.join(ROOT, "docs", "reports",
                                         "phoneme_verification"))
    ap.add_argument("--systems", default="",
                    help="逗号分隔的体系 id 子集（默认全部 11 家）")
    args = ap.parse_args()

    wanted = {s.strip() for s in args.systems.split(",") if s.strip()}
    system_ids = [sid for sid in SCHOLAR_SYSTEMS_ALL
                  if not wanted or sid in wanted]
    os.makedirs(args.out, exist_ok=True)

    md = []
    summary = {"generated": str(date.today()),
               "script": "scripts/phoneme_verification_report.py",
               "systems": {}, "legacy": {},
               "sentences": [{"text": t, "source": s} for t, s in SENTENCES],
               "polyphone_rows": 0}
    all_verif_rows = []
    all_cand_rows = []

    md.append("# 逐音素合成验证报告（学者拟音 → 音频）")
    md.append("")
    md.append("> 生成日期：%s · 脚本 `scripts/phoneme_verification_report.py`（重跑即再生）"
              % summary["generated"])
    md.append("> 数据：`data/historical/sinica_ccr_import/`（Sinica CCR 11 家学者体系）"
              "+ 东汉实验字表（%d 字，`phonology_db.EASTERN_HAN_DB`）。"
              % len(EASTERN_HAN_DB))
    md.append(">")
    md.append("> **核心口径：「有音频输出」≠ 成功。** 引擎对一条读法的处置分档：")
    md.append("> `full` 全部音素按预期合成；`approx` 段完整但个别音素近似（重音/音色丢失）；")
    md.append("> `partial` 含引擎**无法如实发音**的音素（2026-11-03 -x 音素转储实测：")
    md.append("> 多数被替换成声门塞音 [ʔ]、个别整段静默；朗读时按最接近音素近似替代，音色自然、音值近似）；")
    md.append("> `untested` 含未实测音素（不保证）；`silent` 整条无声。")
    md.append("> 能力矩阵来自 `language/phoneme_capability.py`（eSpeak-ng 1.52 -v zh")
    md.append("> 2026-10-30 逐符号实测冻结集合，2026-11-03 -x 复核），矩阵只保证「该段有声音」，不保证听感正确。")
    md.append("")
    md.append("## 一、体系总览")
    md.append("")
    md.append("| 体系 | 字数 | 读法数 | 缺IPA行 | eSpeak full | approx | partial(缺段) | untested | silent | 共振峰 full/partial/silent | 全净字 | 有缺段字 |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|")

    # 阶段 1：全部体系算完（总览表先整体成型，再写各体系详细段落）
    computed = []
    for sid in system_ids:
        name = SCHOLAR_SYSTEMS_ALL[sid]
        readings = load_scholar_readings(sid)
        cap = system_capability_report(sid)
        tokens, levels, formant, n = _collect_system_tokens(readings)
        assert levels == {k: cap[{"full": "espeak_full", "approx": "espeak_approx",
                                  "partial": "espeak_partial",
                                  "untested": "espeak_untested",
                                  "silent": "espeak_silent"}[k]]
                          for k in levels}, sid
        n_silent_tok = sum(t["count"] for t in tokens.values()
                           if t["espeak"] == "silent")
        n_approx_tok = sum(t["count"] for t in tokens.values()
                           if t["espeak"] in ("approx",))
        n_untested_tok = sum(t["count"] for t in tokens.values()
                             if t["espeak"] == "untested")
        md.append("| %s（%s） | %d | %d | %d | %d | %d | %d | %d | %d | %d/%d/%d | %d | %d |" % (
            name, sid, cap["characters"], cap["readings"],
            cap["no_ipa_records"], cap["espeak_full"], cap["espeak_approx"],
            cap["espeak_partial"], cap["espeak_untested"], cap["espeak_silent"],
            cap["formant_full"], cap["formant_partial"], cap["formant_silent"],
            cap["characters_clean"], cap["characters_with_gaps"]))
        summary["systems"][sid] = {
            "name": name,
            "characters": cap["characters"], "readings": cap["readings"],
            "no_ipa_records": cap["no_ipa_records"],
            "espeak": {k: levels[k] for k in levels},
            "formant": dict(formant),
            "tokens": len(tokens),
            "token_counts": {"silent": n_silent_tok, "approx": n_approx_tok,
                             "untested": n_untested_tok,
                             "ok": sum(t["count"] for t in tokens.values()
                                       if t["espeak"] == "ok")},
        }

        # ---- 多音字（该体系，样本句选音与线上同一路径）----
        idx = _index_by_char(sid)
        pol = _polyphone_chars(idx)
        sel_rows = _run_sentence_selections(sid)
        method_count = {"empirical": 0, "fallback_first": 0, "other": 0}
        for r in sel_rows.values():
            if r["method"] == "empirical":
                method_count["empirical"] += 1
            elif r["method"] == "fallback_first":
                method_count["fallback_first"] += 1
            else:
                method_count["other"] += 1
        summary["systems"][sid]["polyphone_chars"] = len(pol)
        summary["systems"][sid]["selection_rows"] = len(sel_rows)
        summary["systems"][sid]["method_count"] = method_count

        computed.append(dict(sid=sid, name=name, readings=readings, cap=cap,
                             tokens=tokens, levels=levels, formant=formant,
                             n_silent_tok=n_silent_tok, n_approx_tok=n_approx_tok,
                             n_untested_tok=n_untested_tok, pol=pol,
                             sel_rows=sel_rows, method_count=method_count))

    # 阶段 2：各体系详细段落
    for c in computed:
        sid, name = c["sid"], c["name"]
        cap, levels, formant = c["cap"], c["levels"], c["formant"]
        md.append("")
        md.append("### %s（%s）" % (name, sid))
        md.append("")
        md.append("- 级别分布：full %d · approx %d · partial %d · untested %d · silent %d"
                  "（按读法计数；共振峰 full %d / partial %d / silent %d）"
                  % (levels["full"], levels["approx"], levels["partial"],
                     levels["untested"], levels["silent"],
                     formant["full"], formant["partial"], formant["silent"]))
        md.append("- 音素级损失：被丢弃（无声）%d 次 · 近似 %d 次 · 未实测 %d 次"
                  % (c["n_silent_tok"], c["n_approx_tok"], c["n_untested_tok"]))
        md.append("- 原始拟音示例（声母/韵母为 Sinica 原值）：")
        md.append("")
        md.append("| 字 | 声母 | 韵母 | IPA 组合 |")
        md.append("|---|---|---|---|")
        md.extend(_raw_examples(c["readings"]))
        md.append("")
        md.append("逐音素矩阵（按损失程度排序；例字最多 3 个）：")
        md.append("")
        _rows, lines = _token_table(c["tokens"])
        md.extend(lines)
        md.append("")

        md.append("多音字：%d 字（≥2 条非 suspect 行）；样本句命中选音 %d 条"
                  "（empirical %d / fallback_first %d / 其他 %d）。"
                  % (len(c["pol"]), len(c["sel_rows"]),
                     c["method_count"]["empirical"],
                     c["method_count"]["fallback_first"],
                     c["method_count"]["other"]))
        md.append("")

        for r in sorted(c["sel_rows"].values(),
                        key=lambda x: (x["char"], x["method"])):
            all_verif_rows.append(r)
        for ch in sorted(c["pol"]):
            recs = c["pol"][ch]
            hit = [r for r in c["sel_rows"].values() if r["char"] == ch]
            for i, rec in enumerate(recs):
                all_cand_rows.append({
                    "system_id": sid, "char": ch,
                    "candidate_idx": i, "ipa": rec.ipa,
                    "is_fallback_first": i == 0,
                    "rhyme_group": rec.rhyme_group,
                    "upstream_note": rec.upstream_note,
                    "source_sheet": rec.source_sheet,
                    "source_row": rec.source_row,
                    "sentence_hit": hit[0]["method"] if hit else "",
                    "selected_ipa": hit[0]["selected_ipa"] if hit else "",
                })

    # ---- 旧实验字表 ----
    ltokens, llevels, lformant, lchars = _legacy_tokens()
    summary["legacy"] = {
        "name": "han_eastern_experimental",
        "characters": lchars,
        "espeak": {k: llevels[k] for k in llevels},
        "formant": dict(lformant),
        "tokens": len(ltokens),
        "token_counts": {
            k: sum(t["count"] for t in ltokens.values() if t["espeak"] == k)
            for k in ("silent", "approx", "untested", "ok")},
    }
    md.append("")
    md.append("## 二、东汉实验字表（han_eastern_experimental，%d 字）" % lchars)
    md.append("")
    md.append("- 级别分布：full %d · approx %d · partial %d · untested %d · silent %d"
              % (llevels["full"], llevels["approx"], llevels["partial"],
                 llevels["untested"], llevels["silent"]))
    md.append("- 注：此表是 v5 之前的实验数据，学者体系接入后仅作对照，"
              "**不得**作为拟音依据。")
    md.append("")
    md.append("逐音素矩阵：")
    md.append("")
    _rows, lines = _token_table(ltokens)
    md.extend(lines)
    md.append("")

    # ---- 多音字人工核验集说明 ----
    md.append("## 三、多音字人工核验集")
    md.append("")
    md.append("语义约定（与 UI/测试一致）：")
    md.append("")
    md.append("- **empirical** = 经验性选择：jieba 分词 → pypinyin 现代声调 →")
    md.append("  中古调类映射 → 广韵音韵地位 → 无歧义字经验投票确认。**不是学者确认**，")
    md.append("  是当前数据规则下的最优经验推断，必须人工抽核。")
    md.append("- **fallback_first** = 不可判定时回退首条非 suspect 行，")
    md.append("  `note` 逐条写明卡在哪一步（声调不可判定 / 无该调类地位 /")
    md.append("  地位类无一致读法 / 一致读法与本字行不符），不猜测。")
    md.append("- 现代声调→中古四声**不是 1:1**：3 声→{上,入}、4 声→{去,入}，")
    md.append("  上/去 与 入声无法再分，这是卡因之一而非缺陷。")
    md.append("")
    md.append("样本句（%d 条，公版古籍）：" % len(SENTENCES))
    md.append("")
    md.append("| 句 | 出处 |")
    md.append("|---|---|")
    for t, s in SENTENCES:
        md.append("| %s | %s |" % (_esc(t), s))
    md.append("")
    md.append("完整核验清单：`polyphone_verification.csv`（逐选音一条，"
              "末两列留空供人工判定）；全部候选行：`polyphone_candidates.csv`"
              "（含韵部、上游备注、来源行号；`is_fallback_first` 标出回退目标行；"
              "约 5 MB，不入库，重跑本脚本即可再生）。")
    md.append("")
    summary["polyphone_rows"] = len(all_verif_rows)
    summary["candidates_rows"] = len(all_cand_rows)

    # ---- 边界声明 ----
    md.append("## 四、边界与如实声明")
    md.append("")
    md.append("1. `approx` 只保证「有声音」，不保证听感正确（重音/音色丢失是已知损失）。")
    md.append("2. `untested` = 不在 2026-10-30 实测冻结集合里的符号，发声与否不保证；")
    md.append("   若表中出现 >0，说明数据里出现了新符号，应补测后更新冻结集合。")
    md.append("3. `no_ipa_records`（缺 IPA 行）= 上游源表缺陷（声母列含汉字/元音开头/")
    md.append("   只剩送气符），加载时如实标记 suspect、不生成 IPA、不参与合成。")
    md.append("4. 共振峰引擎只是 eSpeak 整体失败时的回退，其 partial/silent 占比")
    md.append("   不代表主路径质量。")
    md.append("5. 本报告是数据快照；Sinica 数据包或能力冻结集合变化后重跑本脚本。")
    md.append("6. 逐音素矩阵的 token 粒度 = `sound_synth.tokenize_ipa` 的切分")
    md.append("   （如 `tɣ`、`i̯uŋ`），与引擎实际送读单位一致。")
    md.append("")

    # ---- 写文件 ----
    rep_path = os.path.join(args.out, "REPORT.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    verif_path = os.path.join(args.out, "polyphone_verification.csv")
    with open(verif_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system_id", "char", "method", "selected_ipa",
                    "occurrences", "example_sentence", "note",
                    "人工判定(正确/错误/无法判定)", "核验备注"])
        for r in sorted(all_verif_rows,
                        key=lambda x: (x["system_id"], x["char"], x["method"])):
            w.writerow([r["system_id"], r["char"], r["method"],
                        r["selected_ipa"], r["occurrences"], r["example"],
                        r["note"], "", ""])

    cand_path = os.path.join(args.out, "polyphone_candidates.csv")
    with open(cand_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system_id", "char", "candidate_idx", "ipa",
                    "is_fallback_first", "rhyme_group", "upstream_note",
                    "source_sheet", "source_row",
                    "sentence_hit_method", "selected_ipa"])
        for r in sorted(all_cand_rows,
                        key=lambda x: (x["system_id"], x["char"],
                                       x["candidate_idx"])):
            w.writerow([r["system_id"], r["char"], r["candidate_idx"],
                        r["ipa"], int(r["is_fallback_first"]),
                        r["rhyme_group"], r["upstream_note"],
                        r["source_sheet"], r["source_row"],
                        r["sentence_hit"], r["selected_ipa"]])

    json_path = os.path.join(args.out, "summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("已生成：%s" % args.out)
    for p in (rep_path, verif_path, cand_path, json_path):
        print("  - %s" % p)
    print("多音字核验行 %d，候选行 %d。" % (len(all_verif_rows),
                                           len(all_cand_rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
