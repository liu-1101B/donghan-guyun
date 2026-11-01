# 发音质量验证报告（Pronunciation Quality Validation）

- 日期: 2026-11-03 · 分支 `feat/historical-phonology-foundation`（v5 donghan-guyun）
- 驱动: `scripts/qa_pronunciation_audit.py`（map | collision | polyphone | baseline | all；对语料只读，全部输出可再生）
- 目标: 按四步闭环验证发音质量，**不新增音韵数据**：
  1. 一字跨体系碰撞（原始 IPA → 近似 IPA → 真实音频）；
  2. 对比批量：近似层是否把本来不同的音并成一个；
  3. 多音字人工审核集：量化选择器 + 降低 `fallback_first` 依赖；
  4. 真实设备音频基线（Windows 已完成；Jetson 见 §5.2，需用户设备）。

---

## 0. 验证环境（诚实层前置）

| 项 | 值 |
|---|---|
| 平台 | Windows 11 (10.0.26200, SP0)，win32 |
| 引擎 | 自带 `espeak-ng\espeak-ng.exe`（**eSpeak NG 1.52-dev**，数据 `espeak-ng\espeak-ng-data`） |
| 调用 | 与生产完全一致：`-v zh -p 50 -s 140 -w <wav>`，输入为空格连接的 `[[...]]` 段 |
| 语音 | `zh` 无独立 conf，**即 cmn 语音**：`language cmn/zh-cmn/zh`，`phonemes cmn`，`dictionary cmn`（1.5MB 词典），`pitch 80 118`，无 phoneme 覆盖 |
| 语料 | Sinica CCR 导入 378,214 行（6 中古体系：wangli/dongtonghe/zhoufagao/lifanggui/chenxinxiong/karlgren + 东汉 legacy） |
| 确定性 | 全部输出字节级可复现（多音字选择跨运行稳定，如 傳·王力 `ȡǐwɛn \| ȡǐwɛn \| ȶǐwɛn`） |

**CI 不是真实发音验证**：`.github/workflows/historical-phonology-tests.yml`（windows + ubuntu，Py3.12）当前 152 OK / 4 skipped；
其中 3 个真实引擎测试由 `_bundled_espeak_exe()` 守卫（CI 无自带 espeak 二进制 → 跳过）。CI 验证的是数据与逻辑，**不验证听感**；
本报告的全部"听感"结论来自本地自带 1.52-dev 二进制的实测音频（WAV 时长 + SHA256 固化），pins 仅对该构建有效。

---

## 1. 步骤 1+2：跨体系碰撞（原始 IPA → 近似 IPA → 真实音频）

产物: `collision_table.md`（55 字 × 7 体系，362 个音频样本全部合成成功；
每格 = 该体系首个非 suspect 行 IPA → 近似串 + 实测时长；`qa_audio/collision/manifest.json` 固化 SHA256 + duration，WAV 已 gitignore）。

**近似层并音总账**（`map_collisions.md`，1321 条 IPA 串）——回答"哪些学者记号被并成同一个音"：

| eSpeak 串 | 被并的原始符号 | 感知影响（实测可闻） |
|---|---|---|
| `S` | ś, ɕ, ʂ, ʃ, ṣ | 最大并音组：硬颚(ɕ/ʃ)/卷舌(ʂ/ṣ)/带符(ś)全并——卷舌色彩丢失是主要损失（基线 b14 ʃɑŋ 868.1ms = b15 ʂɑŋ 868.1ms，完全同音） |
| `a` | å, æ, ɐ, ậ, ă | 元音并 a：舌位前后/开口度差异丢失（行 ɣɐŋ vs ɣɑŋ 区分度大降）；ă 为 2026-11-03 用户批准并入（修复前为整符丢失） |
| `r` | ɖ, ɽ, ḍ | 卷舌浊塞/擦/塞擦全并为齿舌浊 r（周法高 ɖ 与李方桂 ḍ 不可分） |
| `Z` | ź, ʑ, ʒ | 浊擦音并 Z |
| `ts` | ȡ, ȶ | 塞擦音别名 ts，**与数据原生双字母 ts 跨层并音**（王力 载 tsɒi / 参 tsʰɒm） |
| `h` | ɦ, ʰ | 浊化与送气两个特征不再区分（引擎侧行为见 §4） |
| `t` | ʈ, ṭ | 卷舌清塞并 t，舌尖位置丢失 |

另有 10 处"跨层并音"（映射产物与原生 ASCII 同串，如 ɣ→x 与原生 x、ɑ→A 与原生 A）与
7 个**未映射透传符号**（â, ï, 及组合附加符 ́/̆/̈/̌/̯）——ă 原在此列，后果经 §4 实测后于 2026-11-03 由用户批准 ă→a 入映射。

**跨体系差异压缩结论**：同一字在 6 体系间的差异主要发生在**声母部位**（ȡ/ȶ/ʈ/ḍ/ȡʰ…）与**元音色**（ɑ/ɐ/ɛ/æ…）；
近似层把前者并到 4–5 档、后者并到 2–3 档。听感上：体系间仍可区分（声母大类与音节骨架保留），
但"王力 vs 周法高"这类细部位差异（舌面前 vs 卷舌）不可闻。这是近似层的设计代价，已量化为并音组表。

---

## 2. 步骤 3：多音字人工审核集

产物: `polyphone_review.md` / `.json`（测试集 `tests/data/polyphone_review.json` v1：27 条目 × 6 体系 = 162 单元格；
另 18 个单读安全字 × 6 = 108 自动核对行）。

### 2.1 总账

- **89 PASS / 54 FAIL / 18 observe / 1 no_data**（162 单元格）
- method 分布（162 审核 + 108 自动）：empirical=53，**fallback_first=162**，single=55 ——
  162 个 fallback_first 说明**多音字路径几乎全部落在"按首条读"的兜底**，这是下一步要压缩的主目标。
- 单读安全字：107 pass / 0 FAIL / 1 more_candidates（**稱**·zhoufagao：数据有 2 条近重复行 `tɕʰieŋ` / `tɕʰiɪŋ`，
  选中 `tɕʰiɪŋ`，属数据层近重复，非选择器缺陷）。

### 2.2 54 FAIL 逐条归因（全部探针复核过）

| 条目 | FAIL 数 | 机制 | 标记 |
|---|---|---|---|
| xing-ping（行·三人行） | 1 | 仅 karlgren：empirical 按现代调 2→平、地位 匣開二庚平 选 ɣɐŋ，与该条目期望集不符 | 无 |
| xing-qu（行·行伍） | 5 | 5 体系按首条 ɣɑŋ 读（平式）；该地位类在数据中无"行伍"去声读法 → 机制够不到 | KNOWN_LIMITATION |
| le-ru（樂·不亦樂乎） | 6 | 现代调 4→去/入、地位 疑肴去，empirical 选 ŋau（乐 lè 去式）；**入声 lɑk 在候选中但从调类 4 不可达**——中古入声字现代调类漂移的典型案例 | KNOWN_LIMITATION |
| chang-shang（長·年長） | 6 | 现代调 3→上/入、地位 知開陽上，同类字一致读为 ȶ(徹母) 而年長是 ȡ(澄母)——**地位类粗于声母区分**，一致读法选到隔壁声母 | 无（真缺口） |
| shuo-ru（說·詩雲） | 6 | 去声游說路径占据地位类，入声 yuè 读法机制够不到 | KNOWN_LIMITATION |
| jue-ru（覺·覺悟） | 6 | 同型：入声觉悟读法从现代调不可达 | KNOWN_LIMITATION |
| zai-qu（載·載歌載舞） | 6 | 地位 精咍去/從咍去 两可，一致读法选 tsɒi(精母) 而期望 dzɒi(從母)——**同地位类跨声母** | 无（真缺口） |
| chuan-ping（傳·傳習錄） | 6 | 广韵表**无属平声调类的地位行** → 回退首条 ȡǐwɛn(去式)——数据覆盖缺口 | 无（数据缺口） |
| e-ru（惡·恶人先告狀） | 6 | 一致读法 ɑŋ 与 惡 各行均不相符 → 回退首条 ʔuo；入声 ɑk 在候选中但兜底不选非首条 | AMBIGUOUS |
| shu-ru（數·數見不失信） | 6 | 入声读数（suk/ʃɔk）在候选中，但**广韵表无属入声调类的地位行** → fallback_first 回退首条 ʃǐu/ʃjuo/ʂiuo/ṣju/ʂi̯u | KNOWN_LIMITATION |

**分类**：54 = **19 未标记（真缺口，进入选择器/数据工作项）** + **29 KNOWN_LIMITATION（机制已知够不到，量化用）** + **6 AMBIGUOUS（数据本身歧义）**。
前两类已带 `flag` 固化在测试集内；终审流程见 `polyphone_review.md` 末节（expected 改 ok/changed → 重跑）。

### 2.3 数据质量发现（NFD）

Sinica 导入 JSON 的 IPA 为 **NFD 分解形**（如 `i` + 组合符 ˆ），与预组合形比较会假 FAIL；
比较/展示层统一 `_nfc()`（曾消除 13 个假 FAIL），**合成输入保持 RAW** 以与生产管线字节一致。

### 2.4 诚实层声明

- expected 读数由**模型预填**（按中古音理标注），**尚未经人耳/师承终审**；FAIL 中至少 chang-shang / zai-qu 两组
  的"期望本身"也应在终审中复核（地位类 vs 声母的粗粒度问题是选择器与测试集共同暴露的）。
- 能力矩阵维持 raw-SILENT（只测能力不猜结果）；读数数据零改动；近似是引擎侧行为，未写回任何数据字段。

---

## 3. 送气/擦音 digraph 专题（原"θ 疑点"，已关闭）

背景：近似层把 ʰ 映为 `h`，送气音经管线变成 `t+h / p+h / k+h / t+s+h` 等串。
早期曾怀疑 zh 语音把 `th` 读成 θ、`ph` 读成 f、`kh` 读成 x（按 base1 单字母表的推断）。
**该怀疑已证伪**，证据链如下（捆绑 1.52-dev 二进制实测 + espeak-ng master 源码佐证）：

### 3.1 语音表来源

`phontab` 为编译产物（58KB 二进制）。源码对照：espeak-ng master（HEAD `4224475`）`phsource/phonemes`
中 `phonemetable cmn base1` + `include ph_cmn`——cmn 集**整体覆盖 base1 单字母名**，改用拼音式声母名：

| cmn 集定义（ph_cmn） | 含义 |
|---|---|
| `ph` = `vls blb stp WAV(ustop/p_asp)` | **送气清双唇塞 pʰ**（非 f） |
| `kh` = `vls uvl stp WAV(ustop/k_asp)` | **送气清软腭塞 kʰ**（非 x） |
| `th` = `vls alv stp` | 齿龈塞（拼音 t = tʰ）（非 θ） |
| `tsh` = `alv afr sib WAV(ustop/ts)` | 塞擦音（拼音 ch） |
| `ts.` / `ts.h` | 卷舌 ts / 卷舌送气 ts |
| `tS;` / `tS;h` / `S;` / `s.` | ipa tɕ / tɕh / ɕ / 卷舌 |

### 3.2 捆绑二进制 -x 实测（-v zh，生产参数）

- `[[tA]] [[thA]] [[pA]] [[phA]] [[kA]] [[khA]] [[sA]] [[tshA]]` 全部按预期切分：`thA55_ / phA55_ / khA55_ / tshjua55n_ …`；
  `th / ph / kh / tsh` 被词法识别为**单个声母音素**。
- **时长 A/B**（同一元音 A 控制，差值 = 辅音差异）：

| 对 | 不送气 | 送气 | Δms |
|---|---|---|---|
| t / th | 712.9 | 746.1 | **+33.2** |
| p / ph | 728.3 | 749.0 | **+20.7** |
| k / kh | 723.1 | 771.7 | **+48.6** |
| s / tsh | 756.8 | 809.6 | +52.8（塞擦音更长，合理） |

→ 送气爆破在 zh 语音中**可闻**（与基线 b24 tʰɑŋ 830.2 / b25 kʰɑŋ 855.8 / b26 bʰɑ 771.1 / b27 pʰɑ 747.0 一致）。

### 3.3 语料影响盘点（6 体系 ʰ 总计 **25,534** 个读数，全部实测拼写路径）

语料送气字面拼写为 `辅音+ʰ`（两字符前缀扫描确认），经 `APPROX→IPA_MAP` 后进入引擎：

| 类 | 计数 | 管线产物 | 引擎行为 | 判定 |
|---|---|---|---|---|
| tʰ / pʰ / kʰ | 2345 / 2590 / 4617 | th / ph / kh | cmn 送气塞 | ✓ 正确 |
| tsʰ（拼写 t+s+ʰ） | 2529 | tsh | cmn 塞擦音 | ✓ 正确 |
| ȶʰ / ȡʰ / ʈʰ | 1031 / 1137 / 303 | tsh / tsh / th | 塞擦 / 送气塞 | ✓ |
| tɕʰ / tʃʰ / tʂʰ | 1031 / 771 / 249 | t+S+h | 塞+硬颚擦+送气 | ✓（tʂʰ 卷舌→硬颚，部位轻度漂移，可闻可辨） |
| dzʰ / dʒʰ / dʐʰ / ʑʰ | 1269 / 485 / 55 / 196 | d+z/h / d+Z/h | 浊塞+擦+送气 | ✓ 近似 |
| bʰ / dʰ / ɡʰ | 2228 / 2378 / 1700 | b/d/g + h | 塞+送气 | ✓ |
| bvʰ / fʰ / ʂʰ / iʰ | 361 / 219 / 39 / 1 | v+h / f+h / S+h | ✓ | 边缘类，无碍 |

**结论：送气在全部 ~25.5k 读数上保留，无系统性丢失；无 θ/f/x 误读。**
`ʰ→h` 冻结映射**维持不变**（不盲改）；本专题结论作为引擎侧词法行为的实测档案归档。

---

## 4. 引擎侧实测缺陷清单（-x + 语料计数，最终版）

| # | 符号 | 语料计数 | 后果 | 严重度 |
|---|---|---|---|---|
| 1 | **ă (U+0103)** | **697**（全部 lifanggui；皆韻系开音节 kăi/kăn/ɣăm/kăt…，kăi 最多 42 条） | 修复前**元音整体丢失**：`kăi` → 合成 [ki55]；**2026-11-03 用户批准 ă→a 后已修复**，697 条元音恢复（碰撞表 山·李方桂格 690ms 异常 → 854ms，与他系同音） | **已修复** |
| 2 | ʔ (U+0294) | ~4500（dong 1375 / zhou 1386 / chen 1368 / karlgren 371） | 喉塞起点丢失；eSpeak 无 ʔ 音素 | 低（听感影响小） |
| 3 | 组合附加符（́ ̆ ̈ ̌ ̯） | 大量 | 无声丢失；声调信息本就统一 55 处理（zh 语音单声调设计） | 已文档化 |
| 4 | ɻ / ɻ̩ / ᴇ (U+1D07) | **0**（语料无出现） | 当前无后果；未来数据引入时的陷阱（基线 b40 ɕiᴇm / b45 ȶiᴇn 已按风险样本固化） | 潜在 |
| 5 | â / ï（未映射透传） | 6 / 3 | 捆绑二进制下透传为带符元音，实测可合成（collision 表内时长正常）；非 ASCII 透传的长期风险 | 观察 |

**修复建议（不擅动冻结映射，决定权在用户）**：
- ă→`a`（ESPEAK_APPROX_MAP 加一行）：**2026-11-03 用户批准并已实施**，与 ɐ→a、æ→a 并音同层。实测效果：碰撞表 山·李方桂格由 690ms 异常读数变为 854ms `San`（与其余 5 体系完全同音，山字并音对 5→9）；karlgren 的 ă 为 NFD 分解形（a+U+0306），元音本可读、仅声符丢失，不受本次修复影响。
- ʔ：无低成本修复（eSpeak 无对应音素；可考虑空实现+文档），维持现状。

---

## 5. 步骤 4：真实设备音频基线

### 5.1 Windows（已完成）

`baseline_win32.md` + `qa_audio/baseline_win32/manifest.json`：**46/46 样本 OK**，每条固化 SHA256 + duration_ms，
元数据含 espeak 版本（1.52-dev）、采样率、构建路径、日期（2026-11-01）。
覆盖：8 元音/鼻韵、入声韵尾、擦音三部位（x/ʃ/ʂ/ʐ/z）、塞擦音三系（ts/tɕ/tʂ，含送气）、浊塞送气（bʰ/dʰ）、
冻结近似同形对照（ɣ vs x、ɖ vs r、ɳ vs n、ɲ vs j）、真实词（東/行/山/道/難/得/切）、三词连读。
关键对照时长：ɑŋ 744.6 = ɔŋ 744.6（ɔ→o 并音实证）；ʃɑŋ 868.1 = ʂɑŋ 868.1（S 并音实证）；ɣɑŋ 861.2 = xɑŋ 861.2。

### 5.2 Jetson（**显式推迟，需用户设备**）

Jetson 不在本机。步骤：在 Jetson 上以同样自带 espeak 运行
`python scripts/qa_pronunciation_audit.py baseline --os-tag jetson`（若该构建 espeak 与 Windows 捆绑版
**同版本**，可用 manifest SHA256 逐条比对；**不同版本则时长 pin 不可移植**，只能听感 + 时长相对比较）。
用户设备就绪后执行并回传 `baseline_jetson.md` + manifest 即可闭环。

### 5.3 声明

CI 绿（152 OK）≠ 真实发音验证；本报告的听感结论绑定 **Windows 自带 1.52-dev 构建**，
换构建需重跑 baseline（pins 不跨构建承诺）。

---

## 6. 结论与建议（按优先级）

1. **发音质量闭环（本机范围）已关闭**：跨体系差异压缩已量化（§1）；多音字 54 FAIL 全部归因（§2.2）；
   送气专题证伪 θ 疑点并实测保留（§3）；引擎缺陷清单收敛为 ă(697) + ʔ(4500, 轻微)（§4）。
2. **已决（2026-11-03）**：`ă→a` 已加入 ESPEAK_APPROX_MAP，全部 QA 产物已重跑（碰撞表 山·李方桂格 690→854ms；基线 46 pins 无 ă 样本、全部不变；审核集数值不变）。
3. **待用户设备**：Jetson baseline（§5.2 指令已备）。
4. **下一步工作项（本轮不做）**：压缩 162 个 fallback_first —— 优先攻 19 个未标记 FAIL 暴露的两类机制
   （地位类粗于声母：長/載；广韵表缺行：傳）；expected 终审（模型预填 → 人耳/师承）；
   称·zhoufagao 近重复数据行去重。
5. **不变项**：能力矩阵 raw-SILENT；读数数据零改动；近似层仅在引擎侧；main(aeab9aa) 不合并、不 rebase、不 force-push。

## 7. 产物清单（全部可由 `scripts/qa_pronunciation_audit.py` 再生）

| 文件 | 内容 |
|---|---|
| `docs/reports/pronunciation_audit/REPORT.md` | 本报告 |
| `docs/reports/pronunciation_audit/map_collisions.md` | 近似层并音组 + 跨层并音 + 未映射透传 |
| `docs/reports/pronunciation_audit/collision_table.md` | 55 字 × 7 体系 原始→近似→音频时长 |
| `docs/reports/pronunciation_audit/polyphone_review.md` / `.json` | 多音字 27 条 × 6 体系审核 + 108 自动行 |
| `docs/reports/pronunciation_audit/baseline_win32.md` | Windows 46 样本基线 |
| `tests/data/polyphone_review.json` | 人工审核测试集 v1（27 条 + 18 安全字；flag 固化） |
| `qa_audio/{collision,baseline_win32}/manifest.json` | 音频 SHA256 + 时长固化（WAV gitignored） |
