# -*- coding: utf-8 -*-
"""发音质量验证闭环 QA 脚本（只读数据，全部输出可再生）。

用户优先级（2026-11-03）：不急着加音韵数据，先把发音质量验证闭环关掉。
本脚本对应四步：

1. ``map``        —— 映射级冲突矩阵（任务②a）：哪些不同学者符号被近似层
   映射到同一个 eSpeak 音素串，按数据出现频次与实例标注。
2. ``collision``  —— 跨体系同字碰撞表（任务①②b）：一个字在 东汉(legacy)/
   王力/董同龢/周法高/李方桂/陳新雄/高本漢 下的原始 IPA → 近似后 IPA →
   真实 eSpeak 音频（时长+wav），并标记"原本不同、近似后相同"的体系对。
3. ``polyphone``  —— 人工审核多音字测试集（任务③）：跑
   tests/data/polyphone_review.json（行/重/乐/长/得 + 扩展字，每条带
   期望读法与选择理由），输出 method 分布与逐条 PASS/FAIL/observe。
4. ``baseline``   —— 真实音频回归基线（任务④）：固定词条 → WAV +
   manifest（sha256/时长/平台/引擎版本）。Windows 本机可跑；Jetson
   Linux 需要该设备上可用的 espeak-ng（仓库捆绑版是 Windows 构建）。

子命令:  map | collision | polyphone | baseline | all
输出目录:
  docs/reports/pronunciation_audit/   —— 报告（md + 小 json），应提交
  qa_audio/                           —— wav + manifest，不提交（见 .gitignore）

约定: 控制台不打印非 ASCII（GBK 安全）；所有结果写文件后用 read 查看。
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import datetime
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import sound_synth as ss                                        # noqa: E402
from language import phoneme_capability as pc                   # noqa: E402
from language.history.sinica_scholar_data import (              # noqa: E402
    SCHOLAR_SYSTEMS, lookup_scholar_reading)
from language.polyphone import select_reading                   # noqa: E402
from phonology_db import EASTERN_HAN_DB                         # noqa: E402

REPORT_DIR = os.path.join(ROOT, "docs", "reports", "pronunciation_audit")
AUDIO_DIR = os.path.join(ROOT, "qa_audio")

MC_SYSTEMS = list(SCHOLAR_SYSTEMS)  # 6 中古体系，保持字典序

# 审核字（37）：行重樂長得 + 用户点名扩展 + 报告多音字高频字
REVIEW_CHARS = list(
    "行重樂長得說為華率王朝中道難好發覺空曲血稱數落種都還"
    "乘載彈便差幹傳會相參惡泊")
# 高频单读字（18）：跨体系碰撞表的"普通字"对照组
HF_CHARS = list("東山水之日月人大天地馬風雨木金火田年")
COLLISION_CHARS = REVIEW_CHARS + HF_CHARS  # 55 字，无重叠


def _clean(recs):
    return [r for r in recs if not r.suspect and r.ipa]


def approx_display(ipa):
    """与合成管线一致：preprocess_ipa 再 _espeak_approx。"""
    return ss._espeak_approx(ss.preprocess_ipa(ipa))


def _nfc(s):
    """Unicode NFC 归一化。

    学者数据存在 NFD 分解形式（如 重·王力 ȡ+i+U+030C+woŋ，2026-11-03 实测
    确认 nfc==raw 为 False），人工标注的期望串常用预组合（U+01D0）——
    直接比较会误报 FAIL。比较/展示前统一 NFC；**送入合成的字符串保持原样**
    （生产管线收到什么就发什么，不改变实测行为）。
    """
    return unicodedata.normalize("NFC", s) if isinstance(s, str) else s


def espeak_ok():
    p = ss.get_espeak_path()
    return bool(p) and os.path.isabs(p) and os.path.exists(p)


def synth_wav(ipa, wav_path, pitch=130):
    """合成单个 IPA 词条，写 wav，返回 (duration_ms, sha256) 或 None。"""
    audio = ss.synthesize_text(ipa, word_gap=0.08, pitch=pitch)
    if audio is None or len(audio) == 0:
        return None
    data = ss.audio_to_wav_bytes(audio, ss.SAMPLE_RATE)
    with open(wav_path, "wb") as f:
        f.write(data)
    ms = len(audio) / ss.SAMPLE_RATE * 1000.0
    return ms, hashlib.sha256(data).hexdigest()


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote %s (%d bytes)" % (os.path.relpath(path, ROOT), len(text.encode("utf-8"))))


# ============================================================
# 1. 映射级冲突矩阵
# ============================================================

def _effective(ch):
    """单个符号进入 eSpeak 前的最终字符串（与管线一致）。"""
    return pc.ESPEAK_APPROX_MAP.get(ch, pc.ESPEAK_IPA_MAP.get(ch, ch))


def _corpus_ipas():
    """全部干净 IPA 串：6 中古体系 + 东汉 legacy。"""
    out = []
    for ch in COLLISION_CHARS:
        for sid in MC_SYSTEMS:
            for r in _clean(lookup_scholar_reading(ch, sid)):
                out.append((ch, sid, r.ipa))
    for ch, rec in EASTERN_HAN_DB.items():
        ipa = rec.get("ipa") if isinstance(rec, dict) else None
        if ipa:
            out.append((ch, "han_eastern(legacy)", ipa))
    return out


def _symbol_occurrences(corpus, limit=6):
    occ = {}
    for ch, sid, ipa in corpus:
        for s in set(ipa):
            occ.setdefault(s, []).append((ch, sid, ipa))
    for s in occ:
        occ[s] = occ[s][:limit]
    return occ


# 组级感知影响注记（人工，键=组内成员集合的排序字符串）
# 组级感知影响注记（人工）。键=成员集合（frozenset），查表用“最大子集”匹配：
# 语料不同 → 组成员不同（如本语料无 ʅ/ç，S 组只含 ś ɕ ʂ ʃ ṣ 五个成员）。
GROUP_NOTES = {
    frozenset("śɕʂʃṣ"): "清擦音最大并音组：硬颚(ɕ/ʃ)、卷舌(ʂ/ṣ)、带符(ś)全并 S——"
                  "李方桂 ṣ(率/数) 与周法高 ʂ、王力 ɕ 听感相同；卷舌色彩丢失是主要损失。",
    frozenset("ʒʐźẓ"): "浊擦音并音组：ʒ/ʐ/ź/ẓ 全并 Z。",
    frozenset("ɖɽḍ"): "卷舌浊塞/擦/塞擦音全并为齿舌浊 r：周法高 ɖ(重/长/传/朝) 与"
                "李方桂 ḍ 不可分。",
    frozenset("ȶȡ"): "硬腭/齿龈-硬腭塞擦音 → 塞擦音别名 ts：与数据里原生双字母 ts"
                "（王力 载 tsɒi、参 tsʰɒm）跨层并音，见下方 ASCII 并层表。",
    frozenset("ʈṭ"): "卷舌清塞 ʈ/ṭ→t：周法高 朝/中 ʈ、李方桂 朝/长 ṭ 与 得 t 合并，"
                "舌尖位置丢失。",
    frozenset("ɳṇ"): "卷舌鼻音 ɳ/ṇ→n：与普通过 n 合并，舌尖位置丢失。",
    frozenset("ɲȵ"): "硬颚鼻 ɲ(冻结) 与 ȵ(常规映射) 跨层并到同一 eSpeak 音素 J，"
                "硬颚鼻与腭化鼻不可分。",
    frozenset("äåæɐʌɤậ"): "带符/近央元音一律并 a：李方桂 å/æ/ậ、王力 ɐ 等——"
                   "舌位前后与开口度差异丢失（行 ɣɐŋ vs ɣɑŋ 的区分度大降）。",
    frozenset("åæɐậ"): "元音并 a 组（本语料实测四个成员）：李方桂 å/æ/ậ、王力 ɐ 全并 a——"
                   "舌位前后与开口度差异丢失（行 ɣɐŋ vs ɣɑŋ 的区分度大降）。",
    frozenset("æɐ"): "前/近央元音 æ/ɐ→a：开口度与舌位差异丢失（行 ɣɐŋ vs ɣɑŋ）。",
    frozenset("źʑʒ"): "浊硬颚/齿龈/带符擦音 ʑ/ʒ/ź 全并 Z（本语料无卷舌浊 ʐ/ẓ）。",
    frozenset("ɔ"): "后半开 ɔ→o（ESPEAK_IPA_MAP 修复映射）：与数据里原生 o 并层"
               "（周法高 覺 kok），乐 ŋɔk 的 ɔ 段变 o。",
    frozenset("ɪ"): "近音 ɪ→i：开口度差异丢失（蒸韵 iɪŋ 的 ɪ 段）。",
    frozenset("ɡ"): "唯一真静默符号：浊软腭 ɡ→g，与 legacy g 并层"
               "（中古数据基本无 ɡ，风险低）。",
    frozenset("ɦʰ"): "ɦ(浊) 与 ʰ(送气) 都映到 h：浊化与送气两个特征不再区分；"
               "且 ʰ 并入辅音后（tʰ→th、tʂʰ→tsh）依赖 eSpeak 词法切分，"
               "“th” 是否按 θ 读取需以 -x 实测为准（见 REPORT.md 附录）。",
    frozenset("ɱ"): "双唇鼻 ɱ→m。",
    frozenset("ɟʎ"): "硬颚浊塞/塞边→j：与零声母 j(为) 合并，声母信息丢失。",
    frozenset("ɨ"): "前高央 ɨ→“1”（eSpeak 重音记号）。",
    frozenset("ə"): "央元音 ə→@（eSpeak 标准 schwa 别名，正常）。",
    frozenset("ɛ"): "前半开 ɛ→E（eSpeak 标准别名，正常）。",
    frozenset("ɑ"): "开后央 ɑ→A（eSpeak 标准别名，正常）。",
}


def _note_for(members):
    """最大子集匹配注记。"""
    m = frozenset(members)
    best, blen = "", -1
    for key, note in GROUP_NOTES.items():
        if key <= m and len(key) > blen:
            best, blen = note, len(key)
    return best


def cmd_map():
    corpus = _corpus_ipas()
    occ = _symbol_occurrences(corpus)
    groups = {}
    for s in occ:
        if s.isascii() and s.isalnum():
            continue  # ASCII 字母数字本身不与任何映射冲突
        groups.setdefault(_effective(s), []).append(s)
    coll = {k: v for k, v in groups.items() if len(v) > 1}

    n_ipa = len(corpus)
    lines = ["# 映射级冲突矩阵（近似层并音分析）", "",
             "- 生成: `scripts/qa_pronunciation_audit.py map`，%s" %
             datetime.date.today().isoformat(),
             "- 语料: %d 审核字 × 6 中古体系 + 东汉 legacy，共 %d 条 IPA 串" %
              (len(REVIEW_CHARS) + len(HF_CHARS), n_ipa),
             "- 规则: 每符号最终 eSpeak 串 = ESPEAK_APPROX_MAP.get(ch, ESPEAK_IPA_MAP.get(ch, ch))",
             "- 类型: approx=28 符号冻结近似层；map=7 修复映射；pass=原生透传（未实测）", "",
             "## 并音组（≥2 个原始符号 → 同一 eSpeak 串）", "",
             "| eSpeak 串 | 原始符号(类型) | 实例(字/体系/IPA) | 感知影响 |",
             "|---|---|---|---|"]
    for key in sorted(coll, key=lambda k: -len(coll[k])):
        members = sorted(coll[key])
        desc = ", ".join("%s(%s)" % (
            m, "approx" if m in pc.ESPEAK_APPROX_MAP
            else ("map" if m in pc.ESPEAK_IPA_MAP else "pass")
            ) for m in members)
        ex = []
        for m in members[:3]:
            for ch, sid, ipa in occ[m][:2]:
                ex.append("%s·%s `%s`" % (ch, sid, _nfc(ipa)))
        note = _note_for(members)
        lines.append("| `%s` | %s | %s | %s |" % (
            key, desc, "; ".join(ex[:4]), note))

    # ASCII 并层：某符号的有效串（含多字母如 ts）与数据里原生 ASCII 串相同
    # → 跨层并音（不同来源的符号在 eSpeak 侧变成同一个音素）。
    effective_ascii = {}   # ascii_str -> set(原始符号)
    for s in occ:
        if s.isascii() and s.isalnum():
            continue
        e = _effective(s)
        if e.isascii() and e.isalnum():
            effective_ascii.setdefault(e, set()).add(s)
    # 语料里以原生形式出现的 ASCII 字母（各 IPA 串中的 ASCII 字母）
    native_letters = {c for s in occ for c in s if c.isascii() and c.isalnum()}
    # 语料各有效串中连续出现的 ASCII 双字母（digraph）
    native_digraphs = set()
    for s in occ:
        e = _effective(s)
        for i in range(len(e) - 1):
            pair = e[i:i + 2]
            if pair[0].isascii() and pair[1].isascii() and pair.isalnum():
                native_digraphs.add(pair)
    ascii_rows = []
    for e in sorted(effective_ascii):
        natives = [c for c in e if c in native_letters]
        dig = e in native_digraphs
        if not natives and not dig:
            continue
        members = sorted(effective_ascii[e])
        ex = []
        for m in members[:2]:
            for ch, sid, ipa in occ[m][:1]:
                ex.append("%s·%s `%s`" % (ch, sid, _nfc(ipa)))
        if dig and len(e) == 2:
            tgt = "原生双字母 %s（语料有效串中直接出现）" % e
        else:
            tgt = "原生字母 %s" % ",".join(natives)
        ascii_rows.append((e, members, tgt, ex))
    lines += ["", "## ASCII 并层（映射产物与原生 ASCII 同串，跨层并音）", ""]
    if ascii_rows:
        lines.append("| eSpeak 串 | 原始符号 | 与之并层的原生形式 | 实例 |")
        lines.append("|---|---|---|---|")
        for e, members, tgt, ex in ascii_rows:
            lines.append("| `%s` | %s | %s | %s |" % (
                e, ", ".join(members), tgt, "; ".join(ex[:2])))
    else:
        lines.append("（无）")

    # 未映射且非 ASCII 的透传符号（风险清单）
    unmapped = sorted(s for s in occ
                      if not (s.isascii() and s.isalnum())
                      and s not in pc.ESPEAK_APPROX_MAP
                      and s not in pc.ESPEAK_IPA_MAP)
    lines += ["", "## 未映射透传符号（非 ASCII，未经 -x 实测，可能被引擎吞掉或误读）", ""]
    if unmapped:
        lines.append("| 符号 | 次数上限 | 实例 |")
        lines.append("|---|---|---|")
        for s in unmapped:
            ex = "; ".join("%s·%s `%s`" % (ch, sid, _nfc(ipa)) for ch, sid, ipa in occ[s][:2])
            lines.append("| %s | %d | %s |" % (s, len(occ[s]), ex))
    else:
        lines.append("（无）")
    lines += ["", "## 说明", "",
              "- 本表回答“哪些原本不同的学者记号，在近似层之后变得相同”。",
              "- 跨层并音（如 ɲ(冻结) 与 ȵ(常规) 同到 J、ȶ/ȡ→ts 与原生 ts）：",
              "  前者在并音组内以成员形式列出，后者见上方 ASCII 并层表。",
              "- pass 型透传符号是否被 eSpeak 如实发音未经 -x 验证，见上风险清单",
              "  （预组合带符元音 â/ï/ă 与组合附加符号 ́/̆/̈/̌/̯ 均在其中）。",
              ""]
    _write(os.path.join(REPORT_DIR, "map_collisions.md"), "\n".join(lines))
    print("map: %d collision groups, %d unmapped pass-through symbols" % (len(coll), len(unmapped)))


# ============================================================
# 2. 跨体系同字碰撞表（含真实音频）
# ============================================================

def _primary(ch, sid):
    recs = _clean(lookup_scholar_reading(ch, sid))
    if not recs:
        return None
    distinct = sorted({r.ipa for r in recs})
    return recs[0].ipa, distinct


def cmd_collision():
    audio_ok = espeak_ok()
    wav_dir = os.path.join(AUDIO_DIR, "collision")
    if audio_ok:
        os.makedirs(wav_dir, exist_ok=True)

    rows = []          # 表行
    manifest = []      # json
    collapse_lines = []
    n_audio = 0
    idx = 0
    for ch in COLLISION_CHARS:
        cells = {}
        for sid in MC_SYSTEMS:
            p = _primary(ch, sid)
            cells[sid] = (p[0] if p else None, p[1] if p else None)
        legacy_rec = EASTERN_HAN_DB.get(ch)
        legacy_ipa = legacy_rec.get("ipa") if isinstance(legacy_rec, dict) else None

        row = {"char": ch, "systems": {}, "legacy": None}
        for sid in MC_SYSTEMS:
            ipa, distinct = cells[sid]
            cell = {"ipa": ipa, "n_distinct": len(distinct) if distinct else 0,
                    "distinct": distinct, "approx": None, "ms": None, "wav": None}
            if ipa:
                cell["approx"] = approx_display(ipa)
                if audio_ok:
                    idx += 1
                    wav = os.path.join(wav_dir, "%02d_%s_%s.wav" % (idx, ch, sid))
                    res = synth_wav(ipa, wav)
                    if res:
                        ms, sha = res
                        cell["ms"], cell["wav"] = round(ms, 1), os.path.relpath(wav, ROOT)
                        n_audio += 1
                        manifest.append({"char": ch, "system": sid, "ipa": ipa,
                                         "approx": cell["approx"], "wav": os.path.relpath(wav, ROOT),
                                         "sha256": sha, "duration_ms": round(ms, 1)})
            row["systems"][sid] = cell
        if legacy_ipa:
            lcell = {"ipa": legacy_ipa, "approx": approx_display(legacy_ipa),
                     "ms": None, "wav": None}
            if audio_ok:
                idx += 1
                wav = os.path.join(wav_dir, "%02d_%s_legacy.wav" % (idx, ch))
                res = synth_wav(legacy_ipa, wav)
                if res:
                    ms, sha = res
                    lcell["ms"], lcell["wav"] = round(ms, 1), os.path.relpath(wav, ROOT)
                    n_audio += 1
                    manifest.append({"char": ch, "system": "han_eastern(legacy)",
                                     "ipa": legacy_ipa, "approx": lcell["approx"],
                                     "wav": os.path.relpath(wav, ROOT),
                                     "sha256": sha, "duration_ms": round(ms, 1)})
            row["legacy"] = lcell
        rows.append(row)

        # 碰撞对统计
        vals = [(sid, cells[sid][0]) for sid in MC_SYSTEMS if cells[sid][0]]
        vals = vals + [(s, ipa) for s, ipa in [("han_eastern(legacy)", legacy_ipa)] if ipa]
        collapsed = []
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                (sa, aa), (sb, ab) = vals[i], vals[j]
                if aa != ab and approx_display(aa) == approx_display(ab):
                    collapsed.append("%s×%s: %s≠%s → 均变 `%s`" % (
                        sa, sb, aa, ab, approx_display(aa)))
        if collapsed:
            collapse_lines.append("- **%s**（%d 对并音）: %s" % (ch, len(collapsed), "; ".join(collapsed)))
        elif len(vals) >= 2:
            collapse_lines.append("- %s: %d 体系均覆盖，无并音" % (ch, len(vals)))

    # 写报告
    name_of = {sid: name for sid, name in SCHOLAR_SYSTEMS.items()}
    L = ["# 跨体系同字碰撞表（原始 IPA → 近似 IPA → 真实音频）", "",
         "- 生成: `scripts/qa_pronunciation_audit.py collision`，%s" % datetime.date.today().isoformat(),
         "- 字集: 55 字（37 审核字 + 18 高频字），体系: 东汉(legacy) + 6 中古体系",
         "- 音频引擎: %s" % (ss.get_espeak_path() if audio_ok else "不可用（本机跳过音频，仅 IPA 对照）"),
         "- 每格 = 该体系首个非 suspect 行的 IPA；括号内为该字在此体系的不同读数个数",
         "- 时长 = 真实 eSpeak 合成样本数换算（含 80ms 词间留白），同一引擎内可横向比较", ""]
    L.append("| 字 | " + " | ".join("东汉" if False else name_of[s] for s in MC_SYSTEMS) + " | 东汉(legacy) |")
    L.append("|" + "---|" * (len(MC_SYSTEMS) + 2))
    for row in rows:
        t = ["**%s**" % row["char"]]
        for sid in MC_SYSTEMS:
            c = row["systems"][sid]
            if not c["ipa"]:
                t.append("—")
            else:
                s = "`%s`→`%s`" % (_nfc(c["ipa"]), c["approx"])
                if c["n_distinct"] > 1:
                    s += " (×%d)" % c["n_distinct"]
                if c["ms"] is not None:
                    s += " [%dms]" % round(c["ms"])
                t.append(s)
        lg = row["legacy"]
        t.append(("`%s`→`%s`%s" % (_nfc(lg["ipa"]), lg["approx"],
                 " [%dms]" % round(lg["ms"]) if lg["ms"] else "")) if lg else "—")
        L.append("| " + " | ".join(t) + " |")

    L += ["", "## 碰撞对（原本不同 → 近似后相同）", ""]
    L += collapse_lines if collapse_lines else ["（无）"]
    n_collapse_chars = sum(1 for x in collapse_lines if "对并音" in x)
    L += ["", "## 汇总", "",
          "- 覆盖 55 字；产生并音对的字: %d；音频样本: %d（%s）" % (
              n_collapse_chars, n_audio, "OK" if audio_ok else "SKIPPED"),
          "- 并音 = 该字在某两体系下原始 IPA 不同、但近似后字符串相同（听感上趋同，"
          "实际听感差异仍需以 wav 试听为准）",
          "- 时长列是同一构建的 eSpeak 输出，可横向比较“哪个体系读得更长/更短”，"
          "但跨 OS/引擎版本不可比（见 baseline manifest）", ""]
    _write(os.path.join(REPORT_DIR, "collision_table.md"), "\n".join(L))
    with open(os.path.join(AUDIO_DIR, "collision", "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"espeak": ss.get_espeak_path(), "platform": platform.platform(),
                   "python": sys.version.split()[0], "samples": manifest},
                  f, ensure_ascii=False, indent=1)
    print("collision: %d chars, %d audio samples (%s)" % (len(rows), n_audio, "OK" if audio_ok else "SKIPPED"))


# ============================================================
# 3. 人工审核多音字测试集
# ============================================================

def cmd_polyphone():
    ds_path = os.path.join(ROOT, "tests", "data", "polyphone_review.json")
    with open(ds_path, "r", encoding="utf-8") as f:
        ds = json.load(f)
    systems = ds["systems"]

    results = []
    method_count = {}
    # 3a. 审核条目
    for e in ds["entries"]:
        ch, ctx = e["char"], e["context"]
        exp = e.get("expected")  # 可能为 null（observe）
        row = {"id": e["id"], "char": ch, "context": ctx, "meaning": e.get("meaning", ""),
               "flag": e.get("flag"), "systems": {}}
        for sid in systems:
            sel = select_reading(ch, ctx, sid)
            method_count[sel.method] = method_count.get(sel.method, 0) + 1
            sel_ipa = _nfc(sel.selected.ipa) if sel.selected else None
            acc = None
            if exp is not None:
                acc_raw = (exp.get("acceptable") or {}).get(sid)
                if acc_raw is not None:
                    acc = {_nfc(x) for x in acc_raw}
            if exp is None:
                status = "observe"
            elif acc is None:
                status = "no_data"
            elif sel_ipa in acc:
                status = "pass"
            else:
                status = "FAIL"
            row["systems"][sid] = {
                "selected": sel_ipa, "method": sel.method, "status": status,
                "candidates": sorted({_nfc(r.ipa) for r in sel.candidates
                                      if r.ipa and not r.suspect}),
                "note": sel.note,
            }
        results.append(row)
    # 3b. 单读安全字自动核对
    auto_rows = []
    for ch in ds.get("auto_safe_chars", []):
        for sid in systems:
            recs = _clean(lookup_scholar_reading(ch, sid))
            distinct = sorted({_nfc(r.ipa) for r in recs})
            sel = select_reading(ch, "通用上下文", sid)
            method_count[sel.method] = method_count.get(sel.method, 0) + 1
            sel_ipa = _nfc(sel.selected.ipa) if sel.selected else None
            if len(distinct) == 1:
                status = "pass" if sel_ipa == distinct[0] else "FAIL"
            else:
                status = "more_candidates"
            auto_rows.append({"char": ch, "system": sid, "selected": sel_ipa,
                              "method": sel.method, "distinct": distinct, "status": status})

    # 汇总
    n_review_cells = sum(1 for r in results for s in r["systems"].values())
    n_pass = sum(1 for r in results for s in r["systems"].values() if s["status"] == "pass")
    n_fail = sum(1 for r in results for s in r["systems"].values() if s["status"] == "FAIL")
    n_observe = sum(1 for r in results for s in r["systems"].values() if s["status"] == "observe")
    n_nodata = sum(1 for r in results for s in r["systems"].values() if s["status"] == "no_data")
    n_auto_pass = sum(1 for a in auto_rows if a["status"] == "pass")
    n_auto_fail = sum(1 for a in auto_rows if a["status"] == "FAIL")
    n_auto_more = sum(1 for a in auto_rows if a["status"] == "more_candidates")

    L = ["# 人工审核多音字测试集 —— 选择器评估", "",
         "- 生成: `scripts/qa_pronunciation_audit.py polyphone`，%s" % datetime.date.today().isoformat(),
         "- 测试集: `tests/data/polyphone_review.json`（v%s，人工预填，待终审）" % ds.get("version", 1),
         "- 规则: 期望 = 每体系允许 IPA 集合（按中古调类+语义标注）；selected ∈ 允许集 → PASS",
         "- method 分布（审核 %d 单元格 + 自动 %d 单元格）: %s" % (
             n_review_cells, len(auto_rows),
             ", ".join("%s=%d" % (k, v) for k, v in sorted(method_count.items()))),
         "- 审核条目: %d PASS / %d FAIL / %d observe / %d no_data（共 %d 单元格，%d 条 × %d 体系）" % (
             n_pass, n_fail, n_observe, n_nodata, n_review_cells, len(results), len(systems)),
         "- 单读安全字自动核对: %d pass / %d FAIL / %d more_candidates" % (
             n_auto_pass, n_auto_fail, n_auto_more), ""]
    name_of = {sid: SCHOLAR_SYSTEMS[sid] for sid in systems}
    for r in results:
        L.append("## %s  「%s」 — %s" % (r["id"], r["char"], r["context"]))
        L.append("- 语义: %s" % r["meaning"])
        if r["flag"]:
            L.append("- 标记: **%s**" % r["flag"])
        L.append("")
        L.append("| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |")
        L.append("|---|---|---|---|---|---|")
        for sid in systems:
            s = r["systems"][sid]
            st = s["status"]
            icon = {"pass": "✓", "FAIL": "✗", "observe": "·", "no_data": "○"}[st]
            L.append("| %s | %s | `%s` | %s | %s %s | %s |" % (
                name_of[sid], ", ".join("`%s`" % c for c in s["candidates"]),
                s["selected"] or "—", s["method"], icon, st, (s["note"] or "").replace("\n", " ")))
        L.append("")
    L += ["## 单读安全字（期望=唯一读数，自动核对）", "",
          "| 字 | 体系 | 候选数 | 选中 | method | 判定 |", "|---|---|---|---|---|---|"]
    for a in auto_rows:
        icon = {"pass": "✓", "FAIL": "✗", "more_candidates": "△"}[a["status"]]
        L.append("| %s | %s | %d | `%s` | %s | %s |" % (
            a["char"], a["system"], len(a["distinct"]), a["selected"] or "—",
            a["method"], icon))
    L += ["", "## 待人工终审说明", "",
          "- 期望读法由预填人（模型）按中古音理标注，**尚未经人耳/师承终审**；",
          "- `flag=KNOWN_LIMITATION` 的条目是“机制已知够不到”的缺口（如中古入声字现代调类漂移），",
          "  报告用于量化缺口而非要求选择器通过；",
          "- 终审时把每条 expected 改为 ok / changed，并更新 acceptable 集合后重跑本脚本。", ""]
    _write(os.path.join(REPORT_DIR, "polyphone_review.md"), "\n".join(L))
    _write(os.path.join(REPORT_DIR, "polyphone_review.json"),
           json.dumps({"method_count": method_count, "results": results,
                       "auto": auto_rows}, ensure_ascii=False, indent=1))
    print("polyphone: %d PASS %d FAIL %d observe %d no_data; method=%s" % (
        n_pass, n_fail, n_observe, n_nodata, json.dumps(method_count, sort_keys=True)))


# ============================================================
# 4. 真实音频回归基线
# ============================================================

BASELINE_WORDS = [
    # (id, ipa, 说明)
    ("b01_a", "a", "元音 a"),
    ("b02_ɑ", "ɑ", "元音 ɑ"),
    ("b03_ɑŋ", "ɑŋ", "后鼻 ɑŋ"),
    ("b04_ɔŋ", "ɔŋ", "后鼻 ɔŋ（修复映射 ɔ→o）"),
    ("b05_əŋ", "əŋ", "央鼻 əŋ（修复映射 ə?）"),
    ("b06_uŋ", "uŋ", "后鼻 uŋ"),
    ("b07_iɪŋ", "iɪŋ", "前鼻 iɪŋ（含冻结 ɪ）"),
    ("b08_au", "au", "复元音 au"),
    ("b09_ɛu", "ɛu", "复元音 ɛu"),
    ("b10_ɔu", "ɔu", "复元音 ɔu"),
    ("b11_ɑk", "ɑk", "入声 ɑk"),
    ("b12_iɪt", "iɪt", "入声 iɪt"),
    ("b13_xɑŋ", "xɑŋ", "牙擦 x（与冻结 ɣ→x 同形对照）"),
    ("b14_ʃɑŋ", "ʃɑŋ", "硬颚清擦 ʃ（冻结→S）"),
    ("b15_ʂɑŋ", "ʂɑŋ", "卷舌清擦 ʂ（修复→S，与 ʃ 对照）"),
    ("b16_ʐɑ", "ʐɑ", "卷舌浊擦 ʐ（修复→Z）"),
    ("b17_zɑ", "zɑ", "浊 z（Z 对照）"),
    ("b18_tʂʰɑŋ", "tʂʰɑŋ", "卷舌清塞擦 tʂʰ"),
    ("b19_ɕi", "ɕi", "硬颚清塞擦 ɕi"),
    ("b20_tɕi", "tɕi", "硬颚清塞擦 tɕi"),
    ("b21_tsi", "tsi", "舌尖前清塞擦 ts"),
    ("b22_tsʰi", "tsʰi", "舌尖前清塞擦 tsʰ"),
    ("b23_dzi", "dzi", "舌尖前浊塞擦 dz"),
    ("b24_tʰɑŋ", "tʰɑŋ", "送气清塞 tʰ"),
    ("b25_kʰɑŋ", "kʰɑŋ", "送气清塞 kʰ"),
    ("b26_bʰɑ", "bʰɑ", "送气浊塞 bʰ"),
    ("b27_pʰɑ", "pʰɑ", "送气清塞 pʰ"),
    ("b28_lɑ", "lɑ", "边音 l"),
    ("b29_rɑ", "rɑ", "齿舌浊 r（与冻结 ɖ/ɽ/ḍ→r 同形对照）"),
    ("b30_ɖɑŋ", "ɖɑŋ", "卷舌浊塞 ɖ（冻结→r）"),
    ("b31_ɳɑ", "ɳɑ", "卷舌鼻 ɳ（冻结→n）"),
    ("b32_ɲɑ", "ɲɑ", "硬颚鼻 ɲ（冻结→J）"),
    ("b33_jɑ", "jɑ", "硬颚近音 j（与 ɲ/ȵ→J 对照）"),
    ("b34_wɑ", "wɑ", "半元音 w"),
    ("b35_mɑ", "mɑ", "双唇鼻 m"),
    ("b36_nɑ", "nɑ", "齿鼻 n（与 ɳ/ṇ→n 对照）"),
    ("b37_ɣɑŋ", "ɣɑŋ", "浊牙擦 ɣ（冻结→x；行）"),
    ("b38_tuŋ", "tuŋ", "真实词：東"),
    ("b39_ɣɑŋ_word", "ɣɑŋ", "真实词：行"),
    ("b40_ɕiᴇm", "ɕiᴇm", "真实词：山（含未映射 ᴇ，风险样本）"),
    ("b41_dʑiɪŋ", "dʑiɪŋ", "真实词：蒸韵 dʑiɪŋ"),
    ("b42_dɑu", "dɑu", "真实词：道"),
    ("b43_nɑn", "nɑn", "真实词：難"),
    ("b44_tək", "tək", "真实词：得（入声）"),
    ("b45_ȶiᴇn", "ȶiᴇn", "真实词：切（含冻结 ȶ + 未映射 ᴇ）"),
    ("b46_phrase", "tʂiəŋ ɣɑŋ ɕiᴇm", "词组：張行山（三词连读）"),
]


def cmd_baseline():
    audio_ok = espeak_ok()
    tag = "win32" if os.name == "nt" else platform.system().lower()
    out_dir = os.path.join(AUDIO_DIR, "baseline_%s" % tag)
    os.makedirs(out_dir, exist_ok=True)
    entries = []
    if audio_ok:
        p = ss.get_espeak_path()
        ver = ""
        try:
            import subprocess
            r = subprocess.run([p, "--version"], capture_output=True, timeout=15)
            for stream in (r.stdout, r.stderr):
                try:
                    txt = stream.decode("utf-8", "replace").strip().splitlines()
                except Exception:
                    txt = []
                if txt:
                    ver = txt[0].strip()
                    break
        except Exception:
            pass
        for bid, ipa, note in BASELINE_WORDS:
            wav = os.path.join(out_dir, "%s.wav" % bid)
            res = synth_wav(ipa, wav)
            if res:
                ms, sha = res
                entries.append({"id": bid, "ipa": ipa, "note": note,
                                "wav": os.path.relpath(wav, ROOT),
                                "sha256": sha, "duration_ms": round(ms, 1)})
    manifest = {
        "platform": platform.platform(), "os_tag": tag,
        "python": sys.version.split()[0],
        "espeak_path": ss.get_espeak_path() if audio_ok else None,
        "espeak_version": ver if audio_ok else None,
        "sample_rate": ss.SAMPLE_RATE,
        "date": datetime.date.today().isoformat(),
        "note": "同一构建内横向可比；跨 OS/引擎版本不可比。Jetson 需 Linux 版 eSpeak-ng。",
        "entries": entries,
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    _write(os.path.join(REPORT_DIR, "baseline_%s.md" % tag),
           "\n".join(["# 音频回归基线（%s）" % tag, "",
                      "- espeak: %s" % (manifest["espeak_path"],),
                      "- version: %s" % (manifest["espeak_version"],),
                      "- samples: %d" % len(entries), "",
                      "| id | ipa | 说明 | 时长ms |", "|---|---|---|---|"] +
                     ["| %s | `%s` | %s | %s |" % (e["id"], e["ipa"], e["note"], e["duration_ms"])
                      for e in entries] + [""]))
    print("baseline: %d words, %d synthesized (%s)" % (len(BASELINE_WORDS), len(entries),
                                                        "OK" if audio_ok else "SKIPPED"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["map", "collision", "polyphone", "baseline", "all"])
    a = ap.parse_args()
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    if a.cmd in ("map", "all"):
        cmd_map()
    if a.cmd in ("polyphone", "all"):
        cmd_polyphone()
    if a.cmd in ("baseline", "all"):
        cmd_baseline()
    if a.cmd in ("collision", "all"):
        cmd_collision()


if __name__ == "__main__":
    main()
