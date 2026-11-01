# 映射级冲突矩阵（近似层并音分析）

- 生成: `scripts/qa_pronunciation_audit.py map`，2026-11-01
- 语料: 56 审核字 × 6 中古体系 + 东汉 legacy，共 1321 条 IPA 串
- 规则: 每符号最终 eSpeak 串 = ESPEAK_APPROX_MAP.get(ch, ESPEAK_IPA_MAP.get(ch, ch))
- 类型: approx=28 符号近似层（含 2026-11-03 用户批准的 ă→a）；map=23 修复映射；pass=原生透传（未实测）

## 并音组（≥2 个原始符号 → 同一 eSpeak 串）

| eSpeak 串 | 原始符号(类型) | 实例(字/体系/IPA) | 感知影响 |
|---|---|---|---|
| `a` | å(approx), æ(map), ă(approx), ɐ(map), ậ(approx) | 樂·lifanggui_mc `ngåk`; 覺·lifanggui_mc `kåk`; 說·dongtonghe_mc `ɕjuæi`; 說·dongtonghe_mc `juæt` | 元音并 a 组（本语料实测四个成员）：李方桂 å/æ/ậ、王力 ɐ 全并 a——舌位前后与开口度差异丢失（行 ɣɐŋ vs ɣɑŋ 的区分度大降）。 |
| `S` | ś(approx), ɕ(map), ʂ(map), ʃ(approx), ṣ(approx) | 說·lifanggui_mc `śjwäi`; 說·lifanggui_mc `śjwät`; 說·wangli_mc `ɕǐwɛi`; 說·wangli_mc `ɕǐwɛt` | 清擦音最大并音组：硬颚(ɕ/ʃ)、卷舌(ʂ/ṣ)、带符(ś)全并 S——李方桂 ṣ(率/数) 与周法高 ʂ、王力 ɕ 听感相同；卷舌色彩丢失是主要损失。 |
| `r` | ɖ(approx), ɽ(approx), ḍ(approx) | 重·zhoufagao_mc `ɖiuoŋ`; 重·zhoufagao_mc `ɖiuoŋ`; 日·wangli_mc `ɽǐět`; 人·wangli_mc `ɽǐěn` | 卷舌浊塞/擦/塞擦音全并为齿舌浊 r：周法高 ɖ(重/长/传/朝) 与李方桂 ḍ 不可分。 |
| `Z` | ź(approx), ʑ(map), ʒ(approx) | 乘·lifanggui_mc `dźjəng`; 乘·lifanggui_mc `dźjəng`; 乘·wangli_mc `dʑǐəŋ`; 乘·wangli_mc `dʑǐəŋ` | 浊硬颚/齿龈/带符擦音 ʑ/ʒ/ź 全并 Z（本语料无卷舌浊 ʐ/ẓ）。 |
| `ts` | ȡ(approx), ȶ(approx) | 重·wangli_mc `ȡǐwoŋ`; 重·wangli_mc `ȡǐwoŋ`; 長·wangli_mc `ȶǐaŋ`; 長·dongtonghe_mc `ȶjɑŋ` | 硬腭/齿龈-硬腭塞擦音 → 塞擦音别名 ts：与数据里原生双字母 ts（王力 载 tsɒi、参 tsʰɒm）跨层并音，见下方 ASCII 并层表。 |
| `h` | ɦ(map), ʰ(map) | 下·han_eastern(legacy) `ɦaʔ`; 为·han_eastern(legacy) `ɦʷe`; 重·dongtonghe_mc `ȡʰjuoŋ`; 重·dongtonghe_mc `ȡʰjuoŋ` | ɦ(浊) 与 ʰ(送气) 都映到 h：浊化与送气两个特征不再区分；且 ʰ 并入辅音后（tʰ→th、tʂʰ→tsh）依赖 eSpeak 词法切分，“th” 是否按 θ 读取需以 -x 实测为准（见 REPORT.md 附录）。 |
| `t` | ʈ(approx), ṭ(approx) | 長·zhoufagao_mc `ʈiɑŋ`; 朝·zhoufagao_mc `ʈiæu`; 長·lifanggui_mc `ṭjang`; 朝·lifanggui_mc `ṭjäu` | 卷舌清塞 ʈ/ṭ→t：周法高 朝/中 ʈ、李方桂 朝/长 ṭ 与 得 t 合并，舌尖位置丢失。 |

## ASCII 并层（映射产物与原生 ASCII 同串，跨层并音）

| eSpeak 串 | 原始符号 | 与之并层的原生形式 | 实例 |
|---|---|---|---|
| `A` | ɑ | 原生字母 A | 行·wangli_mc `ɣɑŋ` |
| `a` | å, æ, ă, ɐ, ậ | 原生字母 a | 樂·lifanggui_mc `ngåk`; 說·dongtonghe_mc `ɕjuæi` |
| `h` | ɦ, ʰ | 原生字母 h | 下·han_eastern(legacy) `ɦaʔ`; 重·dongtonghe_mc `ȡʰjuoŋ` |
| `i` | ɪ | 原生字母 i | 率·zhoufagao_mc `ʂiuɪi` |
| `o` | ɔ | 原生字母 o | 樂·wangli_mc `ŋɔk` |
| `r` | ɖ, ɽ, ḍ | 原生字母 r | 重·zhoufagao_mc `ɖiuoŋ`; 日·wangli_mc `ɽǐět` |
| `t` | ʈ, ṭ | 原生字母 t | 長·zhoufagao_mc `ʈiɑŋ`; 長·lifanggui_mc `ṭjang` |
| `ts` | ȡ, ȶ | 原生双字母 ts（语料有效串中直接出现） | 重·wangli_mc `ȡǐwoŋ`; 長·wangli_mc `ȶǐaŋ` |
| `w` | ʷ | 原生字母 w | 万·han_eastern(legacy) `mʷan` |
| `x` | ɣ | 原生字母 x | 行·wangli_mc `ɣɑŋ` |

## 未映射透传符号（非 ASCII，未经 -x 实测，可能被引擎吞掉或误读）

| 符号 | 次数上限 | 实例 |
|---|---|---|
| â | 6 | 行·lifanggui_mc `ɣâng`; 行·lifanggui_mc `ɣâng` |
| ï | 3 | 差·lifanggui_mc `tṣhaï`; 差·lifanggui_mc `tṣhaï` |
| ́ | 2 | 日·lifanggui_mc `ńźjĕt`; 人·lifanggui_mc `ńźjĕn` |
| ̆ | 6 | 為·dongtonghe_mc `ɣjuĕ`; 為·lifanggui_mc `jwĕ` |
| ̈ | 6 | 說·lifanggui_mc `śjwäi`; 說·lifanggui_mc `jiwät` |
| ̌ | 6 | 重·wangli_mc `ȡǐwoŋ`; 重·wangli_mc `ȡǐwoŋ` |
| ̯ | 6 | 重·karlgren_mc `ȡʰi̯woŋ`; 重·karlgren_mc `ȡʰi̯woŋ` |

## 说明

- 本表回答“哪些原本不同的学者记号，在近似层之后变得相同”。
- 跨层并音（如 ɲ(冻结) 与 ȵ(常规) 同到 J、ȶ/ȡ→ts 与原生 ts）：
  前者在并音组内以成员形式列出，后者见上方 ASCII 并层表。
- pass 型透传符号是否被 eSpeak 如实发音未经 -x 验证，见上风险清单
  （预组合带符元音 â/ï 与组合附加符号 ́/̆/̈/̌/̯ 均在其中）。
