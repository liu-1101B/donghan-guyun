# 人工审核多音字测试集 —— 选择器评估

- 生成: `scripts/qa_pronunciation_audit.py polyphone`，2026-11-01
- 测试集: `tests/data/polyphone_review.json`（v1，人工预填，待终审）
- 规则: 期望 = 每体系允许 IPA 集合（按中古调类+语义标注）；selected ∈ 允许集 → PASS
- method 分布（审核 162 单元格 + 自动 108 单元格）: empirical=53, fallback_first=162, single=55
- 审核条目: 89 PASS / 54 FAIL / 18 observe / 1 no_data（共 162 单元格，27 条 × 6 体系）
- 单读安全字自动核对: 107 pass / 0 FAIL / 1 more_candidates

## xing-ping  「行」 — 三人行，必有我師焉
- 语义: 行走、行为（xíng，中古平声）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ɣɐŋ`, `ɣɑŋ` | `ɣɑŋ` | fallback_first | ✓ pass | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑŋ 读，不作调类推断 |
| 董同龢系統 | `ɣɐŋ`, `ɣɑŋ` | `ɣɑŋ` | fallback_first | ✓ pass | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑŋ 读，不作调类推断 |
| 周法高系統 | `ɣaŋ`, `ɣɑn`, `ɣɑŋ` | `ɣɑn` | fallback_first | ✓ pass | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑn 读，不作调类推断 |
| 李方桂系統 | `ɣâng`, `ɣɐng` | `ɣâng` | fallback_first | ✓ pass | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣâng 读，不作调类推断 |
| 陳新雄系統 | `ɣaŋ`, `ɣɑŋ` | `ɣɑŋ` | fallback_first | ✓ pass | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑŋ 读，不作调类推断 |
| 高本漢系統 | `ɣɐŋ`, `ɣɑŋ` | `ɣɐŋ` | empirical | ✗ FAIL | 词「三人行」现代调 2 → 平声；音韵地位 匣開二庚平；同类字一致读 ɣɐŋ |

## xing-qu  「行」 — 行伍
- 语义: 行列（háng，中古去声）
- 标记: **KNOWN_LIMITATION**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ɣɐŋ`, `ɣɑŋ` | `ɣɑŋ` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑŋ 读，不作调类推断 |
| 董同龢系統 | `ɣɐŋ`, `ɣɑŋ` | `ɣɑŋ` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑŋ 读，不作调类推断 |
| 周法高系統 | `ɣaŋ`, `ɣɑn`, `ɣɑŋ` | `ɣɑn` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑn 读，不作调类推断 |
| 李方桂系統 | `ɣâng`, `ɣɐng` | `ɣâng` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣâng 读，不作调类推断 |
| 陳新雄系統 | `ɣaŋ`, `ɣɑŋ` | `ɣɑŋ` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（该音韵地位类无一致读法）；按首条 ɣɑŋ 读，不作调类推断 |
| 高本漢系統 | `ɣɐŋ`, `ɣɑŋ` | `ɣɐŋ` | empirical | ✓ pass | 词「行伍」现代调 2 → 平声；音韵地位 匣開二庚平；同类字一致读 ɣɐŋ |

## chong-qu  「重」 — 慎重大事
- 语义: 重要（zhòng，中古去声）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ȡǐwoŋ` | `ȡǐwoŋ` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ȡǐwok 与本字各行均不相符）；按首条 ȡǐwoŋ 读，不作调类推断 |
| 董同龢系統 | `ȡʰjuoŋ` | `ȡʰjuoŋ` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ȡʰjuok 与本字各行均不相符）；按首条 ȡʰjuoŋ 读，不作调类推断 |
| 周法高系統 | `ɖiuoŋ` | `ɖiuoŋ` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ɖiuok 与本字各行均不相符）；按首条 ɖiuoŋ 读，不作调类推断 |
| 李方桂系統 | `ḍjwong` | `ḍjwong` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ḍjwok 与本字各行均不相符）；按首条 ḍjwong 读，不作调类推断 |
| 陳新雄系統 | `ȡʰǐuŋ` | `ȡʰǐuŋ` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ȡʰǐuk 与本字各行均不相符）；按首条 ȡʰǐuŋ 读，不作调类推断 |
| 高本漢系統 | `ȡʰi̯woŋ` | `ȡʰi̯woŋ` | fallback_first | ✓ pass | 多音字（2 条）未能确定（一致读法 ȡʰi̯wok 与本字各行均不相符）；按首条 ȡʰi̯woŋ 读，不作调类推断 |

## le-ru  「樂」 — 不亦樂乎
- 语义: 快乐（lè，中古入声药韵）
- 标记: **KNOWN_LIMITATION**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `lɑk`, `ŋau`, `ŋɔk` | `ŋau` | empirical | ✗ FAIL | 词「不亦樂乎」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋau |
| 董同龢系統 | `lɑk`, `ŋau`, `ŋɔk` | `ŋau` | empirical | ✗ FAIL | 词「不亦樂乎」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋau |
| 周法高系統 | `lɑk`, `ŋau`, `ŋok` | `ŋau` | empirical | ✗ FAIL | 词「不亦樂乎」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋau |
| 李方桂系統 | `lâk`, `ngau`, `ngåk` | `ngau` | empirical | ✗ FAIL | 词「不亦樂乎」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ngau |
| 陳新雄系統 | `lɑk`, `ŋɔk`, `ŋɔu` | `ŋɔu` | empirical | ✗ FAIL | 词「不亦樂乎」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋɔu |
| 高本漢系統 | `lɑk`, `ŋau`, `ŋɔk` | `ŋau` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（该音韵地位类无一致读法）；按首条 ŋau 读，不作调类推断 |

## le-qu  「樂」 — 仁者樂山，知者樂水
- 语义: 喜好（yào，中古去声效韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `lɑk`, `ŋau`, `ŋɔk` | `ŋau` | empirical | ✓ pass | 词「樂山」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋau |
| 董同龢系統 | `lɑk`, `ŋau`, `ŋɔk` | `ŋau` | empirical | ✓ pass | 词「樂山」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋau |
| 周法高系統 | `lɑk`, `ŋau`, `ŋok` | `ŋau` | empirical | ✓ pass | 词「樂山」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋau |
| 李方桂系統 | `lâk`, `ngau`, `ngåk` | `ngau` | empirical | ✓ pass | 词「樂山」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ngau |
| 陳新雄系統 | `lɑk`, `ŋɔk`, `ŋɔu` | `ŋɔu` | empirical | ✓ pass | 词「樂山」现代调 4 → 去/入声；音韵地位 疑肴去；同类字一致读 ŋɔu |
| 高本漢系統 | `lɑk`, `ŋau`, `ŋɔk` | `ŋau` | fallback_first | ✓ pass | 多音字（3 条）未能确定（该音韵地位类无一致读法）；按首条 ŋau 读，不作调类推断 |

## chang-ping  「長」 — 長短
- 语义: 长短（cháng，中古平声宕韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ȡǐaŋ`, `ȶǐaŋ` | `ȶǐaŋ` | empirical | ✓ pass | 词「長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶǐaŋ |
| 董同龢系統 | `ȡʰjɑŋ`, `ȶjɑŋ` | `ȶjɑŋ` | empirical | ✓ pass | 词「長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶjɑŋ |
| 周法高系統 | `ɖiɑŋ`, `ʈiɑŋ` | `ʈiɑŋ` | empirical | ✓ pass | 词「長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ʈiɑŋ |
| 李方桂系統 | `ḍjang`, `ṭjang` | `ṭjang` | empirical | ✓ pass | 词「長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ṭjang |
| 陳新雄系統 | `ȡʰǐɑŋ`, `ȶǐɑŋ` | `ȶǐɑŋ` | empirical | ✓ pass | 词「長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶǐɑŋ |
| 高本漢系統 | `ȡʰi̯aŋ`, `ȶi̯aŋ` | `ȶi̯aŋ` | empirical | ✓ pass | 词「長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶi̯aŋ |

## chang-shang  「長」 — 年長
- 语义: 年长、排行（zhǎng，中古上声）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ȡǐaŋ`, `ȶǐaŋ` | `ȶǐaŋ` | empirical | ✗ FAIL | 词「年長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶǐaŋ |
| 董同龢系統 | `ȡʰjɑŋ`, `ȶjɑŋ` | `ȶjɑŋ` | empirical | ✗ FAIL | 词「年長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶjɑŋ |
| 周法高系統 | `ɖiɑŋ`, `ʈiɑŋ` | `ʈiɑŋ` | empirical | ✗ FAIL | 词「年長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ʈiɑŋ |
| 李方桂系統 | `ḍjang`, `ṭjang` | `ṭjang` | empirical | ✗ FAIL | 词「年長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ṭjang |
| 陳新雄系統 | `ȡʰǐɑŋ`, `ȶǐɑŋ` | `ȶǐɑŋ` | empirical | ✗ FAIL | 词「年長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶǐɑŋ |
| 高本漢系統 | `ȡʰi̯aŋ`, `ȶi̯aŋ` | `ȶi̯aŋ` | empirical | ✗ FAIL | 词「年長」现代调 3 → 上/入声；音韵地位 知開陽上；同类字一致读 ȶi̯aŋ |

## de-ru  「得」 — 得失之間
- 语义: 得到（dé，中古入声德韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `tək` | `tək` | single | ✓ pass |  |
| 董同龢系統 | `tək` | `tək` | single | ✓ pass |  |
| 周法高系統 | `tək` | `tək` | single | ✓ pass |  |
| 李方桂系統 | `tək` | `tək` | single | ✓ pass |  |
| 陳新雄系統 | `tək` | `tək` | single | ✓ pass |  |
| 高本漢系統 | `tək` | `tək` | single | ✓ pass |  |

## shuo-qu  「說」 — 游說之士
- 语义: 劝说（shuì，中古去声薛韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `jǐwɛt`, `ɕǐwɛi`, `ɕǐwɛt` | `ɕǐwɛi` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ɕǐwɛi 读，不作调类推断 |
| 董同龢系統 | `juæt`, `ɕjuæi`, `ɕjuæt` | `ɕjuæi` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ɕjuæi 读，不作调类推断 |
| 周法高系統 | `iuæt`, `ɕiuæi`, `ɕiuæt` | `ɕiuæi` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ɕiuæi 读，不作调类推断 |
| 李方桂系統 | `jiwät`, `śjwäi`, `śjwät` | `śjwäi` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 śjwäi 读，不作调类推断 |
| 陳新雄系統 | `ǐuɛt`, `ɕǐuɛi`, `ɕǐuɛt` | `ɕǐuɛi` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ɕǐuɛi 读，不作调类推断 |
| 高本漢系統 | `ɕi̯wɛi`, `ɕi̯wɛt` | `ɕi̯wɛi` | fallback_first | ✓ pass | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 ɕi̯wɛi 读，不作调类推断 |

## shuo-ru  「說」 — 子曰，詩雲
- 语义: 言说（shuō，中古入声薛韵）
- 标记: **KNOWN_LIMITATION**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `jǐwɛt`, `ɕǐwɛi`, `ɕǐwɛt` | `ɕǐwɛi` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（按单字常读；广韵表无属该调类的地位）；按首条 ɕǐwɛi 读，不作调类推断 |
| 董同龢系統 | `juæt`, `ɕjuæi`, `ɕjuæt` | `ɕjuæi` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（按单字常读；广韵表无属该调类的地位）；按首条 ɕjuæi 读，不作调类推断 |
| 周法高系統 | `iuæt`, `ɕiuæi`, `ɕiuæt` | `ɕiuæi` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（按单字常读；广韵表无属该调类的地位）；按首条 ɕiuæi 读，不作调类推断 |
| 李方桂系統 | `jiwät`, `śjwäi`, `śjwät` | `śjwäi` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（按单字常读；广韵表无属该调类的地位）；按首条 śjwäi 读，不作调类推断 |
| 陳新雄系統 | `ǐuɛt`, `ɕǐuɛi`, `ɕǐuɛt` | `ɕǐuɛi` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（按单字常读；广韵表无属该调类的地位）；按首条 ɕǐuɛi 读，不作调类推断 |
| 高本漢系統 | `ɕi̯wɛi`, `ɕi̯wɛt` | `ɕi̯wɛi` | fallback_first | ✗ FAIL | 多音字（2 条）未能确定（按单字常读；广韵表无属该调类的地位）；按首条 ɕi̯wɛi 读，不作调类推断 |

## hua-ping  「華」 — 灼灼其華
- 语义: 花、华美（huá，中古平声麻韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `hwa`, `ɣwa` | `ɣwa` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 hwa、ɣwa 与本字各行均不相符）；按首条 ɣwa 读，不作调类推断 |
| 董同龢系統 | `xua`, `ɣua` | `ɣua` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 xua、ɣua 与本字各行均不相符）；按首条 ɣua 读，不作调类推断 |
| 周法高系統 | `xua`, `ɣua` | `ɣua` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 xua、ɣua 与本字各行均不相符）；按首条 ɣua 读，不作调类推断 |
| 李方桂系統 | `xwa`, `ɣwa` | `ɣwa` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 xwa、ɣwa 与本字各行均不相符）；按首条 ɣwa 读，不作调类推断 |
| 陳新雄系統 | `xua`, `ɣua` | `ɣua` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 xua、ɣua 与本字各行均不相符）；按首条 ɣua 读，不作调类推断 |
| 高本漢系統 | `ɣwa` | `ɣwa` | empirical | ✓ pass | 词「其華」现代调 2 → 平声；音韵地位 匣合二麻平、曉合二麻平；同类字一致读 ɣwa |

## jue-ru  「覺」 — 覺悟
- 语义: 觉悟（jué，中古入声觉韵）
- 标记: **KNOWN_LIMITATION**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `kau`, `kɔk` | `kau` | fallback_first | ✗ FAIL | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 董同龢系統 | `kau`, `kɔk` | `kau` | fallback_first | ✗ FAIL | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 周法高系統 | `kau`, `kok` | `kau` | fallback_first | ✗ FAIL | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 李方桂系統 | `kau`, `kåk` | `kau` | fallback_first | ✗ FAIL | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 陳新雄系統 | `kɔk`, `kɔu` | `kɔu` | fallback_first | ✗ FAIL | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kɔu 读，不作调类推断 |
| 高本漢系統 | `kau`, `kɔk` | `kau` | fallback_first | ✗ FAIL | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |

## jue-qu  「覺」 — 夢覺
- 语义: 睡醒（jué，中古去声）
- 标记: **KNOWN_LIMITATION**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `kau`, `kɔk` | `kau` | fallback_first | ✓ pass | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 董同龢系統 | `kau`, `kɔk` | `kau` | fallback_first | ✓ pass | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 周法高系統 | `kau`, `kok` | `kau` | fallback_first | ✓ pass | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 李方桂系統 | `kau`, `kåk` | `kau` | fallback_first | ✓ pass | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |
| 陳新雄系統 | `kɔk`, `kɔu` | `kɔu` | fallback_first | ✓ pass | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kɔu 读，不作调类推断 |
| 高本漢系統 | `kau`, `kɔk` | `kau` | fallback_first | ✓ pass | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 kau 读，不作调类推断 |

## zai-shang  「載」 — 萬事勝載
- 语义: 记载（zǎi，中古上声贿韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `dzɒi`, `tsɒi` | `tsɒi` | empirical | ✓ pass | 词「萬事勝載」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsɒi |
| 董同龢系統 | `dzʰAi`, `tsAi` | `tsAi` | empirical | ✓ pass | 词「萬事勝載」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsAi |
| 周法高系統 | `dzəi`, `tsəi` | `tsəi` | empirical | ✓ pass | 词「萬事勝載」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsəi |
| 李方桂系統 | `dzậi`, `tsậi` | `tsậi` | empirical | ✓ pass | 词「萬事勝載」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsậi |
| 陳新雄系統 | `dzʰəi`, `tsəi` | `tsəi` | empirical | ✓ pass | 词「萬事勝載」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsəi |
| 高本漢系統 | `dzʰɑ̆i`, `tsɑ̆i` | `tsɑ̆i` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 dzʰɑ̆i、tsɑ̆i 与本字各行均不相符）；按首条 tsɑ̆i 读，不作调类推断 |

## zai-qu  「載」 — 載歌載舞
- 语义: 装载、承载（zài，中古去声泰韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `dzɒi`, `tsɒi` | `tsɒi` | empirical | ✗ FAIL | 词「載歌」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsɒi |
| 董同龢系統 | `dzʰAi`, `tsAi` | `tsAi` | empirical | ✗ FAIL | 词「載歌」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsAi |
| 周法高系統 | `dzəi`, `tsəi` | `tsəi` | empirical | ✗ FAIL | 词「載歌」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsəi |
| 李方桂系統 | `dzậi`, `tsậi` | `tsậi` | empirical | ✗ FAIL | 词「載歌」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsậi |
| 陳新雄系統 | `dzʰəi`, `tsəi` | `tsəi` | empirical | ✗ FAIL | 词「載歌」现代调 4 → 去/入声；音韵地位 精咍去、從咍去；同类字一致读 tsəi |
| 高本漢系統 | `dzʰɑ̆i`, `tsɑ̆i` | `tsɑ̆i` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（一致读法 dzʰɑ̆i、tsɑ̆i 与本字各行均不相符）；按首条 tsɑ̆i 读，不作调类推断 |

## hui-qu  「會」 — 會合
- 语义: 会合（huì，中古去声队韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `kuɑi`, `ɣuɑi` | `ɣuɑi` | fallback_first | ✓ pass | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ɣuɑi 读，不作调类推断 |
| 董同龢系統 | `kuɑi`, `ɣuɑi` | `ɣuɑi` | fallback_first | ✓ pass | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ɣuɑi 读，不作调类推断 |
| 周法高系統 | `kuɑi`, `ɣuɑi` | `ɣuɑi` | fallback_first | ✓ pass | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ɣuɑi 读，不作调类推断 |
| 李方桂系統 | `kwâi`, `ɣwâi` | `ɣwâi` | fallback_first | ✓ pass | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ɣwâi 读，不作调类推断 |
| 陳新雄系統 | `kuai`, `ɣuai` | `ɣuai` | fallback_first | ✓ pass | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ɣuai 读，不作调类推断 |
| 高本漢系統 | `kwɑi`, `ɣwɑi` | `ɣwɑi` | fallback_first | ✓ pass | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ɣwɑi 读，不作调类推断 |

## chuan-qu  「傳」 — 自傳
- 语义: 传记（zhuàn，中古去声愿韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ȡǐwɛn`, `ȶǐwɛn` | `ȡǐwɛn` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡǐwɛn 读，不作调类推断 |
| 董同龢系統 | `ȡʰjuæn`, `ȶjuæn` | `ȡʰjuæn` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡʰjuæn 读，不作调类推断 |
| 周法高系統 | `ɖiuæn`, `ʈiuæn` | `ɖiuæn` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ɖiuæn 读，不作调类推断 |
| 李方桂系統 | `ḍjwän`, `ṭjwän` | `ḍjwän` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ḍjwän 读，不作调类推断 |
| 陳新雄系統 | `ȡʰǐuɛn`, `ȶǐuɛn` | `ȡʰǐuɛn` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡʰǐuɛn 读，不作调类推断 |
| 高本漢系統 | `ȡʰi̯wɛn`, `ȶi̯wɛn` | `ȡʰi̯wɛn` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡʰi̯wɛn 读，不作调类推断 |

## chuan-ping  「傳」 — 傳習錄
- 语义: 传递（chuán，中古平声仙韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ȡǐwɛn`, `ȶǐwɛn` | `ȡǐwɛn` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡǐwɛn 读，不作调类推断 |
| 董同龢系統 | `ȡʰjuæn`, `ȶjuæn` | `ȡʰjuæn` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡʰjuæn 读，不作调类推断 |
| 周法高系統 | `ɖiuæn`, `ʈiuæn` | `ɖiuæn` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ɖiuæn 读，不作调类推断 |
| 李方桂系統 | `ḍjwän`, `ṭjwän` | `ḍjwän` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ḍjwän 读，不作调类推断 |
| 陳新雄系統 | `ȡʰǐuɛn`, `ȶǐuɛn` | `ȡʰǐuɛn` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡʰǐuɛn 读，不作调类推断 |
| 高本漢系統 | `ȡʰi̯wɛn`, `ȶi̯wɛn` | `ȡʰi̯wɛn` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ȡʰi̯wɛn 读，不作调类推断 |

## e-qu  「惡」 — 好逸惡勞
- 语义: 厌恶（wù，中古去声禡韵，零声母）
- 标记: **AMBIGUOUS**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `u`, `ɑk` | `u` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ɑŋ 与本字各行均不相符）；按首条 u 读，不作调类推断 |
| 董同龢系統 | `ʔuo`, `ʔɑk` | `ʔuo` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔuo 读，不作调类推断 |
| 周法高系統 | `ʔuo`, `ʔɑk` | `ʔuo` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔuo 读，不作调类推断 |
| 李方桂系統 | `uo`, `âk` | `uo` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 âng 与本字各行均不相符）；按首条 uo 读，不作调类推断 |
| 陳新雄系統 | `ʔu`, `ʔɑk` | `ʔu` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔu 读，不作调类推断 |
| 高本漢系統 | `ʔuo`, `ʔɑk` | `ʔuo` | fallback_first | ✓ pass | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔuo 读，不作调类推断 |

## e-ru  「惡」 — 惡人先告狀
- 语义: 邪恶（è，中古入声锡韵）
- 标记: **AMBIGUOUS**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `u`, `ɑk` | `u` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（一致读法 ɑŋ 与本字各行均不相符）；按首条 u 读，不作调类推断 |
| 董同龢系統 | `ʔuo`, `ʔɑk` | `ʔuo` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔuo 读，不作调类推断 |
| 周法高系統 | `ʔuo`, `ʔɑk` | `ʔuo` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔuo 读，不作调类推断 |
| 李方桂系統 | `uo`, `âk` | `uo` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（一致读法 âng 与本字各行均不相符）；按首条 uo 读，不作调类推断 |
| 陳新雄系統 | `ʔu`, `ʔɑk` | `ʔu` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔu 读，不作调类推断 |
| 高本漢系統 | `ʔuo`, `ʔɑk` | `ʔuo` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（一致读法 ʔɑŋ 与本字各行均不相符）；按首条 ʔuo 读，不作调类推断 |

## shu-ru  「數」 — 數見不失信
- 语义: 屡次（shuò，中古入声屋韵）
- 标记: **KNOWN_LIMITATION**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `suk`, `ʃǐu`, `ʃɔk` | `ʃǐu` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʃǐu 读，不作调类推断 |
| 董同龢系統 | `suk`, `ʃjuo`, `ʃɔk` | `ʃjuo` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʃjuo 读，不作调类推断 |
| 周法高系統 | `suk`, `ʂiuo`, `ʂok` | `ʂiuo` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʂiuo 读，不作调类推断 |
| 李方桂系統 | `suk`, `ṣju`, `ṣåk` | `ṣju` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ṣju 读，不作调类推断 |
| 陳新雄系統 | `sok`, `ʃǐu`, `ʃɔk` | `ʃǐu` | fallback_first | ✗ FAIL | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʃǐu 读，不作调类推断 |
| 高本漢系統 | `ʂi̯u`, `ʂɔk` | `ʂi̯u` | fallback_first | ✗ FAIL | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ʂi̯u 读，不作调类推断 |

## shu-shang  「數」 — 數目
- 语义: 数目（shù，中古上声语韵）
- 标记: **KNOWN_LIMITATION**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `suk`, `ʃǐu`, `ʃɔk` | `ʃǐu` | fallback_first | ✓ pass | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʃǐu 读，不作调类推断 |
| 董同龢系統 | `suk`, `ʃjuo`, `ʃɔk` | `ʃjuo` | fallback_first | ✓ pass | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʃjuo 读，不作调类推断 |
| 周法高系統 | `suk`, `ʂiuo`, `ʂok` | `ʂiuo` | fallback_first | ✓ pass | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʂiuo 读，不作调类推断 |
| 李方桂系統 | `suk`, `ṣju`, `ṣåk` | `ṣju` | fallback_first | ✓ pass | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ṣju 读，不作调类推断 |
| 陳新雄系統 | `sok`, `ʃǐu`, `ʃɔk` | `ʃǐu` | fallback_first | ✓ pass | 多音字（4 条）未能确定（广韵表无属该调类的地位）；按首条 ʃǐu 读，不作调类推断 |
| 高本漢系統 | `ʂi̯u`, `ʂɔk` | `ʂi̯u` | fallback_first | ✓ pass | 多音字（3 条）未能确定（广韵表无属该调类的地位）；按首条 ʂi̯u 读，不作调类推断 |

## huan-ping  「還」 — 還鄉
- 语义: 返回（huán，中古平声桓韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `zǐwɛn`, `ɣwan` | `ɣwan` | empirical | ✓ pass | 词「還鄉」现代调 2 → 平声；音韵地位 匣合刪平；同类字一致读 ɣwan |
| 董同龢系統 | `zjuæn`, `ɣuan` | `ɣuan` | empirical | ✓ pass | 词「還鄉」现代调 2 → 平声；音韵地位 匣合刪平；同类字一致读 ɣuan |
| 周法高系統 | `ziuæn`, `ɣuan` | `ɣuan` | empirical | ✓ pass | 词「還鄉」现代调 2 → 平声；音韵地位 匣合刪平；同类字一致读 ɣuan |
| 李方桂系統 | `zjwän`, `ɣwan` | `ɣwan` | empirical | ✓ pass | 词「還鄉」现代调 2 → 平声；音韵地位 匣合刪平；同类字一致读 ɣwan |
| 陳新雄系統 | `zǐuɛn`, `ɣuan` | `ɣuan` | empirical | ✓ pass | 词「還鄉」现代调 2 → 平声；音韵地位 匣合刪平；同类字一致读 ɣuan |
| 高本漢系統 | `zi̯wɛn`, `ɣuan` | `ɣuan` | fallback_first | ✓ pass | 多音字（2 条）未能确定（一致读法 ɣwan 与本字各行均不相符）；按首条 ɣuan 读，不作调类推断 |

## can-ping  「參」 — 參加
- 语义: 参与（cān，中古平声侵韵）

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `sɑm`, `tsʰɒm`, `tʃʰǐěm`, `ʃǐěm` | `ʃǐěm` | fallback_first | ✓ pass | 多音字（5 条）未能确定（该音韵地位类无一致读法）；按首条 ʃǐěm 读，不作调类推断 |
| 董同龢系統 | `sɑm`, `tsʰAm`, `tʃʰjem`, `ʃjem` | `ʃjem` | fallback_first | ✓ pass | 多音字（5 条）未能确定（该音韵地位类无一致读法）；按首条 ʃjem 读，不作调类推断 |
| 周法高系統 | `sɑm`, `tsʰem`, `tsʰəm`, `tʂʰiɪm`, `ʂiɪm` | `ʂiɪm` | fallback_first | ✓ pass | 多音字（5 条）未能确定（该音韵地位类无一致读法）；按首条 ʂiɪm 读，不作调类推断 |
| 李方桂系統 | `sâm`, `tshậm`, `tṣhjəm`, `ṣjəm` | `ṣjəm` | fallback_first | ✓ pass | 多音字（5 条）未能确定（该音韵地位类无一致读法）；按首条 ṣjəm 读，不作调类推断 |
| 陳新雄系統 | `sɑm`, `tsʰəm`, `tʃʰǐəm`, `ʃǐəm` | `ʃǐəm` | fallback_first | ✓ pass | 多音字（5 条）未能确定（该音韵地位类无一致读法）；按首条 ʃǐəm 读，不作调类推断 |
| 高本漢系統 | `tsʰɑ̆m`, `tʂʰi̯əm` | `tsʰɑ̆m` | empirical | ○ no_data | 词「參加」现代调 1 → 平声；音韵地位 清覃平；同类字一致读 tsʰɑ̆m |

## cha-ping-observe  「差」 — 參差不齊
- 语义: 参差（cī，中古平声）
- 标记: **OBSERVE_ONLY**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `tʃʰa`, `tʃʰai`, `tʃʰǐe`, `tʃʰɐi` | `tʃʰai` | empirical | · observe | 词「參差」现代调 4 → 去/入声；音韵地位 初開佳去；同类字一致读 tʃʰai |
| 董同龢系統 | `tʃʰa`, `tʃʰje`, `tʃʰæi`, `tʃʰɐi` | `tʃʰæi` | empirical | · observe | 词「參差」现代调 4 → 去/入声；音韵地位 初開佳去；同类字一致读 tʃʰæi |
| 周法高系統 | `tʂʰa`, `tʂʰiɪ`, `tʂʰæi`, `tʂʰɛi` | `tʂʰæi` | empirical | · observe | 词「參差」现代调 4 → 去/入声；音韵地位 初開佳去；同类字一致读 tʂʰæi |
| 李方桂系統 | `tṣha`, `tṣhaï`, `tṣhjĕ`, `tṣhăi` | `tṣhaï` | empirical | · observe | 词「參差」现代调 4 → 去/入声；音韵地位 初開佳去；同类字一致读 tṣhaï |
| 陳新雄系統 | `tʃʰa`, `tʃʰæi`, `tʃʰǐɛ`, `tʃʰɐi` | `tʃʰæi` | empirical | · observe | 词「參差」现代调 4 → 去/入声；音韵地位 初開佳去；同类字一致读 tʃʰæi |
| 高本漢系統 | `tʂʰa`, `tʂʰie̯` | `tʂʰie̯` | fallback_first | · observe | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 tʂʰie̯ 读，不作调类推断 |

## shuai-shang-observe  「率」 — 循率
- 语义: 遵循、率领（shuài，中古上声术韵）
- 标记: **OBSERVE_ONLY**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `ʃwi`, `ʃǐuět` | `ʃwi` | fallback_first | · observe | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ʃwi 读，不作调类推断 |
| 董同龢系統 | `ʃjuei`, `ʃjuet` | `ʃjuei` | fallback_first | · observe | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ʃjuei 读，不作调类推断 |
| 周法高系統 | `ʂiuɪi`, `ʂiuɪt` | `ʂiuɪi` | fallback_first | · observe | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ʂiuɪi 读，不作调类推断 |
| 李方桂系統 | `ṣjuĕt`, `ṣjwi` | `ṣjwi` | fallback_first | · observe | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ṣjwi 读，不作调类推断 |
| 陳新雄系統 | `ʃǐue` | `ʃǐue` | single | · observe |  |
| 高本漢系統 | `ʂi̯uĕt`, `ʂwi` | `ʂwi` | fallback_first | · observe | 多音字（2 条）未能确定（该音韵地位类无一致读法）；按首条 ʂwi 读，不作调类推断 |

## cheng-ping-observe  「乘」 — 乘舟
- 语义: 乘坐（chéng，中古平声蒸韵）
- 标记: **OBSERVE_ONLY**

| 体系 | 候选(非suspect) | 选中 | method | 判定 | 备注 |
|---|---|---|---|---|---|
| 王力系統 | `dʑǐəŋ` | `dʑǐəŋ` | fallback_first | · observe | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 dʑǐəŋ 读，不作调类推断 |
| 董同龢系統 | `dʑʰjəŋ` | `dʑʰjəŋ` | fallback_first | · observe | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 dʑʰjəŋ 读，不作调类推断 |
| 周法高系統 | `ʑieŋ`, `ʑiɪŋ` | `ʑiɪŋ` | fallback_first | · observe | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 ʑiɪŋ 读，不作调类推断 |
| 李方桂系統 | `dźjəng` | `dźjəng` | fallback_first | · observe | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 dźjəng 读，不作调类推断 |
| 陳新雄系統 | `dʑʰǐəŋ` | `dʑʰǐəŋ` | fallback_first | · observe | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 dʑʰǐəŋ 读，不作调类推断 |
| 高本漢系統 | `dʑʰi̯əŋ` | `dʑʰi̯əŋ` | fallback_first | · observe | 多音字（2 条）未能确定（广韵表无属该调类的地位）；按首条 dʑʰi̯əŋ 读，不作调类推断 |

## 单读安全字（期望=唯一读数，自动核对）

| 字 | 体系 | 候选数 | 选中 | method | 判定 |
|---|---|---|---|---|---|
| 王 | wangli_mc | 1 | `ɣǐwaŋ` | fallback_first | ✓ |
| 王 | dongtonghe_mc | 1 | `ɣjuɑŋ` | fallback_first | ✓ |
| 王 | zhoufagao_mc | 1 | `jiuɑŋ` | fallback_first | ✓ |
| 王 | lifanggui_mc | 1 | `jwang` | fallback_first | ✓ |
| 王 | chenxinxiong_mc | 1 | `jǐuɑŋ` | fallback_first | ✓ |
| 王 | karlgren_mc | 1 | `ji̯waŋ` | empirical | ✓ |
| 中 | wangli_mc | 1 | `ȶǐuŋ` | fallback_first | ✓ |
| 中 | dongtonghe_mc | 1 | `ȶjuŋ` | fallback_first | ✓ |
| 中 | zhoufagao_mc | 1 | `ʈiuŋ` | fallback_first | ✓ |
| 中 | lifanggui_mc | 1 | `ṭjung` | fallback_first | ✓ |
| 中 | chenxinxiong_mc | 1 | `ȶǐoŋ` | fallback_first | ✓ |
| 中 | karlgren_mc | 1 | `ȶi̯uŋ` | fallback_first | ✓ |
| 道 | wangli_mc | 1 | `dɑu` | single | ✓ |
| 道 | dongtonghe_mc | 1 | `dʰɑu` | single | ✓ |
| 道 | zhoufagao_mc | 1 | `dɑu` | single | ✓ |
| 道 | lifanggui_mc | 1 | `dâu` | single | ✓ |
| 道 | chenxinxiong_mc | 1 | `dʰɑu` | single | ✓ |
| 道 | karlgren_mc | 1 | `dʰɑu` | single | ✓ |
| 難 | wangli_mc | 1 | `nɑn` | fallback_first | ✓ |
| 難 | dongtonghe_mc | 1 | `nɑn` | fallback_first | ✓ |
| 難 | zhoufagao_mc | 1 | `nɑn` | fallback_first | ✓ |
| 難 | lifanggui_mc | 1 | `nân` | fallback_first | ✓ |
| 難 | chenxinxiong_mc | 1 | `nɑn` | fallback_first | ✓ |
| 難 | karlgren_mc | 1 | `nɑn` | fallback_first | ✓ |
| 好 | wangli_mc | 1 | `hɑu` | empirical | ✓ |
| 好 | dongtonghe_mc | 1 | `xɑu` | empirical | ✓ |
| 好 | zhoufagao_mc | 1 | `xɑu` | empirical | ✓ |
| 好 | lifanggui_mc | 1 | `xâu` | empirical | ✓ |
| 好 | chenxinxiong_mc | 1 | `xɑu` | empirical | ✓ |
| 好 | karlgren_mc | 1 | `xɑu` | empirical | ✓ |
| 發 | wangli_mc | 1 | `pǐwɐt` | single | ✓ |
| 發 | dongtonghe_mc | 1 | `pjuɐt` | single | ✓ |
| 發 | zhoufagao_mc | 1 | `piɑt` | single | ✓ |
| 發 | lifanggui_mc | 1 | `pjwɐt` | single | ✓ |
| 發 | chenxinxiong_mc | 1 | `pfǐuɐt` | single | ✓ |
| 發 | karlgren_mc | 1 | `pi̯wɐt` | single | ✓ |
| 空 | wangli_mc | 1 | `kʰuŋ` | fallback_first | ✓ |
| 空 | dongtonghe_mc | 1 | `kʰuŋ` | fallback_first | ✓ |
| 空 | zhoufagao_mc | 1 | `kʰuŋ` | fallback_first | ✓ |
| 空 | lifanggui_mc | 1 | `khung` | fallback_first | ✓ |
| 空 | chenxinxiong_mc | 1 | `kʰoŋ` | fallback_first | ✓ |
| 空 | karlgren_mc | 1 | `kʰuŋ` | fallback_first | ✓ |
| 曲 | wangli_mc | 1 | `kʰǐwok` | single | ✓ |
| 曲 | dongtonghe_mc | 1 | `kʰjuok` | single | ✓ |
| 曲 | zhoufagao_mc | 1 | `kʰiuok` | single | ✓ |
| 曲 | lifanggui_mc | 1 | `khjwok` | single | ✓ |
| 曲 | chenxinxiong_mc | 1 | `kʰǐuk` | single | ✓ |
| 曲 | karlgren_mc | 1 | `kʰi̯wok` | single | ✓ |
| 血 | wangli_mc | 1 | `hiwet` | single | ✓ |
| 血 | dongtonghe_mc | 1 | `xiuɛt` | single | ✓ |
| 血 | zhoufagao_mc | 1 | `xiuɛt` | single | ✓ |
| 血 | lifanggui_mc | 1 | `xiwet` | single | ✓ |
| 血 | chenxinxiong_mc | 1 | `xiuet` | single | ✓ |
| 血 | karlgren_mc | 1 | `xiwet` | single | ✓ |
| 稱 | wangli_mc | 1 | `tɕʰǐəŋ` | fallback_first | ✓ |
| 稱 | dongtonghe_mc | 1 | `tɕʰjəŋ` | fallback_first | ✓ |
| 稱 | zhoufagao_mc | 2 | `tɕʰiɪŋ` | fallback_first | △ |
| 稱 | lifanggui_mc | 1 | `tśhjəng` | fallback_first | ✓ |
| 稱 | chenxinxiong_mc | 1 | `tɕʰǐəŋ` | fallback_first | ✓ |
| 稱 | karlgren_mc | 1 | `tɕʰi̯əŋ` | fallback_first | ✓ |
| 相 | wangli_mc | 1 | `sǐaŋ` | fallback_first | ✓ |
| 相 | dongtonghe_mc | 1 | `sjɑŋ` | fallback_first | ✓ |
| 相 | zhoufagao_mc | 1 | `siɑŋ` | fallback_first | ✓ |
| 相 | lifanggui_mc | 1 | `sjang` | fallback_first | ✓ |
| 相 | chenxinxiong_mc | 1 | `sǐɑŋ` | fallback_first | ✓ |
| 相 | karlgren_mc | 1 | `si̯aŋ` | fallback_first | ✓ |
| 落 | wangli_mc | 1 | `lɑk` | single | ✓ |
| 落 | dongtonghe_mc | 1 | `lɑk` | single | ✓ |
| 落 | zhoufagao_mc | 1 | `lɑk` | single | ✓ |
| 落 | lifanggui_mc | 1 | `lâk` | single | ✓ |
| 落 | chenxinxiong_mc | 1 | `lɑk` | single | ✓ |
| 落 | karlgren_mc | 1 | `lɑk` | single | ✓ |
| 種 | wangli_mc | 1 | `tɕǐwoŋ` | fallback_first | ✓ |
| 種 | dongtonghe_mc | 1 | `tɕjuoŋ` | fallback_first | ✓ |
| 種 | zhoufagao_mc | 1 | `tɕiuoŋ` | fallback_first | ✓ |
| 種 | lifanggui_mc | 1 | `tśjwong` | fallback_first | ✓ |
| 種 | chenxinxiong_mc | 1 | `tɕǐuŋ` | fallback_first | ✓ |
| 種 | karlgren_mc | 1 | `tɕi̯woŋ` | fallback_first | ✓ |
| 都 | wangli_mc | 1 | `tu` | single | ✓ |
| 都 | dongtonghe_mc | 1 | `tuo` | single | ✓ |
| 都 | zhoufagao_mc | 1 | `tuo` | single | ✓ |
| 都 | lifanggui_mc | 1 | `tuo` | single | ✓ |
| 都 | chenxinxiong_mc | 1 | `tu` | single | ✓ |
| 都 | karlgren_mc | 1 | `tuo` | single | ✓ |
| 彈 | wangli_mc | 1 | `dɑn` | fallback_first | ✓ |
| 彈 | dongtonghe_mc | 1 | `dʰɑn` | fallback_first | ✓ |
| 彈 | zhoufagao_mc | 1 | `dɑn` | fallback_first | ✓ |
| 彈 | lifanggui_mc | 1 | `dân` | fallback_first | ✓ |
| 彈 | chenxinxiong_mc | 1 | `dʰɑn` | fallback_first | ✓ |
| 彈 | karlgren_mc | 1 | `dʰɑn` | fallback_first | ✓ |
| 便 | wangli_mc | 1 | `bǐɛn` | fallback_first | ✓ |
| 便 | dongtonghe_mc | 1 | `bʰjæn` | fallback_first | ✓ |
| 便 | zhoufagao_mc | 1 | `biæn` | fallback_first | ✓ |
| 便 | lifanggui_mc | 1 | `bjiän` | fallback_first | ✓ |
| 便 | chenxinxiong_mc | 1 | `bʰǐɛn` | fallback_first | ✓ |
| 便 | karlgren_mc | 1 | `bʰi̯ɛn` | fallback_first | ✓ |
| 幹 | wangli_mc | 1 | `kɑn` | single | ✓ |
| 幹 | dongtonghe_mc | 1 | `kɑn` | single | ✓ |
| 幹 | zhoufagao_mc | 1 | `kɑn` | single | ✓ |
| 幹 | lifanggui_mc | 1 | `kân` | single | ✓ |
| 幹 | chenxinxiong_mc | 1 | `kɑn` | single | ✓ |
| 幹 | karlgren_mc | 1 | `kɑn` | single | ✓ |
| 泊 | wangli_mc | 1 | `bɑk` | single | ✓ |
| 泊 | dongtonghe_mc | 1 | `bʰɑk` | single | ✓ |
| 泊 | zhoufagao_mc | 1 | `bɑk` | single | ✓ |
| 泊 | lifanggui_mc | 1 | `bâk` | single | ✓ |
| 泊 | chenxinxiong_mc | 1 | `bʰɑk` | single | ✓ |
| 泊 | karlgren_mc | 1 | `bʰɑk` | single | ✓ |

## 待人工终审说明

- 期望读法由预填人（模型）按中古音理标注，**尚未经人耳/师承终审**；
- `flag=KNOWN_LIMITATION` 的条目是“机制已知够不到”的缺口（如中古入声字现代调类漂移），
  报告用于量化缺口而非要求选择器通过；
- 终审时把每条 expected 改为 ok / changed，并更新 acceptable 集合后重跑本脚本。
