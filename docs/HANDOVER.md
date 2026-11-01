# 交接说明（给下一个会话／模型）

> 更新时间：2026-11-03（声音合成修复：eSpeak 临时文件位置 / rc=0 空文件检测 + 共振峰元音表 + 覆盖率表渲染；robot = v5 主界面）　分支：`feat/historical-phonology-foundation`

新会话接手时，先读这一页，再读 [`docs/v5-goal.md`](v5-goal.md)（六阶段路线与逐阶段差距）
和 [`docs/HISTORICAL_PHONOLOGY_ARCHITECTURE.md`](HISTORICAL_PHONOLOGY_ARCHITECTURE.md)（数据与引擎架构）。

## 一、仓库位置与分支

- 仓库根：`donghan-guyin/`，当前根目录检出的是 **`main`**
- 本分支的工作树：**`donghan-guyin/.wt-feat-phon/`** ← 所有开发都在这里
- 分支：`feat/historical-phonology-foundation`
- 状态：**本地 = 远程**（截至 2026-11-03 已推送 `b97a9a7` ← `8a7d037` ← `c067139`；
  8a7d037 = v5 robot 主界面并入，b97a9a7 = 修复 robot 冒烟/CI 细节，
  更早的 5 提交 `1758fe4`/`dae94c1`/`3ad1727`/`804db34`/`0e8ce5e` 均已在链上）。
  推送凭据：一次性 PAT 已存入 Windows 凭据管理器（git credential manager），
  推送若失败先查 `api.github.com` 连通性并重试（github.com:443 链路不稳）。
- 仓库已改名为 **`donghan-guyun`**：origin 现为
  `https://github.com/liu-1101B/donghan-guyun.git`（本地 remote 已更新；旧 URL
  `donghan-guyin` 会 301 重定向但仍可用）
- 本机**没有保存的 GitHub 凭据**（无 GCM 条目、无 SSH 密钥）：后续推送需要
  临时 PAT（一次性 `git push https://x-access-token:<PAT>@github.com/...`，
  勿写入 config，用完即吊销）。直连 github.com:443 通但链路不稳，push 失败时
  重试几次即可（勿配注册表里陈旧的 127.0.0.1:7897 代理，端口没在监听）
- ⚠️ **2026-11-03 推送发现**：一次性 PAT `ghp_qpaG…` 认证有效，但**缺 `workflow` scope**，
  GitHub 拒绝任何包含 `.github/workflows/*` 变更的推送（报错原文：
  “refusing to allow a Personal Access Token to create or update workflow …
  without `workflow` scope”）。待推提交里含 workflow 变更，因此**下一个一次性 PAT 必须带**：
  classic = `repo` + `workflow`；或 fine-grained = “Contents: read and write” +
  “Workflows: read and write”。
- **sinica 索引缓存 / 沙箱边界（2026-11-03）**：`language/history/sinica_ccr_data.py`
  把索引构建写到进程 tempdir（约 197 MB，按源数据 sha 命名
  `donghan_sinica_ccr_<sha24>.sqlite3`）。本沙箱子进程无法重建：TMP/TEMP 被剥掉
  （tempdir 落到 CWD=工作树）、AppData 写被拒、且对 >~12MB 已提交数据建索引
  报 sqlite CANTOPEN（**本地沙箱假象**，CI 的 Linux /tmp 与真机不受影响）。
  已把 2026-10-30 构建的有效缓存（源 sha 与当前数据文件一致，378,214 行）预置在
  **工作树根**同名文件；`.gitignore` 已忽略 `donghan_sinica_ccr_*.sqlite3*` 与
  `jieba.cache`。**不要删工作树根的 196MB 缓存文件**（本地测试靠它）；若数据文件
  sha 变化，需在沙箱外重建或从真机拷贝。
- **CI 轻量依赖集**：`requirements-phonology-tests.txt`（5 个包：
  opencc-python-reimplemented / pypinyin / jieba≥0.42 / numpy / scipy，逐包有理由注释；
  qieyun 故意不含——其测试自跳过）。干净 venv 验证 132 项全过（1 个 qieyun 自跳过）。
  根 `requirements.txt`、`requirements-robot.txt` 已补 opencc / jieba。
- 工作区约定：`run_feat_tests.py`（工作树根，未跟踪，测试运行器，**保留**）

## 二、运行环境（照抄即可）

```powershell
$py = "C:\Users\HP\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
$ws = "C:\Users\HP\Documents\deepseek-harness\default-workspace"
$env:PYTHONPATH = "$ws\.libs_guyun2;$ws\.libs_pyarrow17;$ws\.libs_guyun"
$env:PYTHONUTF8 = "1"; $env:PYTHONIOENCODING = "utf-8"
```

三个目录，顺序重要（**`.libs_guyun2` 必须最先**）：

| 目录 | 内容 | 说明 |
|---|---|---|
| `.libs_guyun2` | numpy 2.5.4、scipy 1.18.1 | 2026-10-30 重建的数值栈（原因见坑 1） |
| `.libs_pyarrow17` | pyarrow 17.0.0 | 仅测试约定用；app 本身用 `.libs_guyun` 里的 pyarrow 26 |
| `.libs_guyun` | 其余全部：streamlit 1.66.1、pandas 3.1.0、pyarrow 26.0.0、pypinyin 0.55.0、jieba 0.42.1（sdist 手工解压）、edge_tts、gTTS、qieyun、vosk、sherpa_onnx、altair、networkx 2.5.1（已打补丁）等 | 主依赖栈 |

依赖安装一律走 `pip_safe.py`（沙箱 0o700 问题），缓存 `--cache-dir .pip_cache`。

### 必须知道的坑（2026-10-30 环境重建后）

1. **numpy 必须 ≥2，`requirements.txt` 里旧的上限注释已作废**
   streamlit 的传递依赖 pandas 3.1.0 硬性要求 numpy ≥ 2.0.2；旧文档钉的
   `numpy<2 + scipy<1.14 + pyarrow<18` 组合与 pandas 3.1.0 不兼容，`st.dataframe`
   直接 ImportError。现行为：numpy 2.5.4 + scipy 1.18.1（在 `.libs_guyun2`）+
   pyarrow 26.0.0（在 `.libs_guyun`），`requirements.txt` 已同步更新。
2. **qieyun 依赖 networkx 2.5.1 的 `np.float_`，numpy 2.0 已移除该别名**
   修复方式：`.libs_guyun\networkx\readwrite\graphml.py` 与 `gexf.py` 各 1 处
   `np.float_` → `np.float64`（语义等价）。**重装 networkx 或换 numpy 时要重新检查
   「切韵对照」能否导入**（`from Qieyun import 字頭2音韻地位_出處們`）。
3. **`.libs_guyun` 里有 `numpy_stale_126` / `scipy_stale_113` / `*.libs_stale` 残留目录**
   旧的 numpy 1.26.4 / scipy 1.13.1 的 `.pyd` 文件被某种 OS 层保护**无法删除也无法写入**
   （icacls 显示用户有 F、无 Deny ACE、无进程占用；`os.remove`/`Remove-Item`/写打开
   全部 Access Denied，但**目录重命名可以**——已改名为 `*_stale*` 移出导入路径）。
   它们是死重量，`import numpy/scipy` 永远解析到 `.libs_guyun2`，不要试图再删，
   也不要让 `.libs_guyun` 排在 `.libs_guyun2` 前面。
4. **跑测试要用工作树根的 `run_feat_tests.py`**（现跑 `test_historical_phonology.py`
   + `test_llm_provider.py` + `test_robot_app_smoke.py`，161 项全绿）
   原生 `python -m unittest` 会有 5 项假失败——沙箱拒绝写入 `tempfile.mkdtemp()`
   创建的 `0o700` 目录，该脚本把 `0o700` 重映射为 `0o707`。
   仓库根的 `run_tests_sandbox.py` **不要**在工作树 CWD 下运行。
   UI 冒烟：`$py scripts/smoke_app.py`（无头 AppTest，检查脚本树无异常 + 拟音体系 selectbox）。
5. **Streamlit 必须带 `--global.developmentMode=false`**
   因为依赖是 `pip --target` 装的，`__file__` 不含 `site-packages`，会被误判成开发模式，
   然后报 `server.port does not work when global.developmentMode is true`。
6. **git 已设 `http.sslBackend=openssl`**
   本机 schannel 后端是坏的（`SEC_E_NO_CREDENTIALS`），openssl 正常。已写入仓库本地配置。

### 其它环境备忘

- 沙箱 pwsh 以 Low Mandatory Level 运行；`whoami`/`tasklist` 走 python 子进程会被拒，
  进程扫描用 `Get-CimInstance Win32_Process`。`.ps1` 脚本在此环境会撞执行策略 /
  PS5.1 解析问题——**用直接一行命令**。
- 工作树文件带旧会话的 label grant（`S-1-4-225216295-…`），当前会话的 grant 只覆盖
  工作区根与部分目录；跨目录写文件若遇 Access Denied，优先换写法（如 pwsh 直写）而非重试。
- 上游数据文件里可能含**分解形式 Unicode**（如 n+U+0301），源码里需要时用显式
  `\uXXXX` 转义且**必须从运行时 `ord()` 实测值抄写**，禁止手拼；不做全局 NFKC。

## 三、v5 路线与当前进度

路线（详见 v5-goal.md）：**一 历史语言体系 → 二 古音资料库 → 三 发音引擎 → 四 智能对话 → 五 机器人交互 → 六 工程化**

用户已定：**先 B（第二阶段）再 A（第三阶段），C 不急**。

### 第二阶段 ✅ 已完成（提交 `5809b41`、`63e146a` 等）

- 接入 Sinica CCR **11 家学者拟音**（中古 6 + 上古 5，PDM，数据包在仓库内），
  加《广韵》反切音韵地位（CC0）、PHONO-ML、中原音韵，共 14 个注册体系。
- 接口：`lookup_reading`、`lookup_scholar_reading`、`scholar_coverage`、
  `compare_character`（同字跨体系对照，值类型三分 ipa/transcription/position）；
  报告 `python scripts/coverage_report.py --all`。
- UI：「🔀 同字跨体系对照（争议项）」展开器 + 各体系覆盖表。
- 数据契约（**不要破坏**）：上游无声调字段 `tone` 恒 `None` 不补全；声母 `0` = 零声母；
  错位行判据「以元音开头」不能改「含元音」（李方桂 `ji-` 喻母会误判 974 行）；
  错位行 `source_record_defect` 且不给 IPA；跳过数必须计数并暴露。

### 第三阶段 ✅ 已完成（三步独立提交 + 本提交）

1. **`text_to_ipa(system_id=...)` 路由**（`4c3c783`）：11 家学者体系可送发音引擎；
   `han_eastern_experimental` ≡ legacy 旧路径；非 IPA 体系抛 `ValueError`；
   学者路径缺字计 unknown，**不补现代拼音**。
2. **IPA→eSpeak 能力矩阵**（`0af9c9f`）：`language/phoneme_capability.py`
   `assess_ipa` / `system_capability_report` / `preprocess_ipa` 重构；
   能读 ≠ 音值正确；eSpeak 逐字丢弃是实测行为；报告数字被测试冻结。
3. **重建可信度 × 合成能力双列 UI**（本提交）：`guyun_app.py`「拟音体系」selectbox
   （默认 + 11 家）；`process_input_scholar` 7 元组；逐字对照表数据侧/引擎侧分列，
   `AncientResult.characters` 逐字明细；合成能力汇总 + 覆盖率 caption；
   音频卡片/下载名随体系动态化。

测试：`run_feat_tests.py` 107 项全绿；
`scripts/smoke_app.py` AppTest 冒烟通过（6 个 selectbox，含「拟音体系」）。

> 2026-11-03 起该能力已**同步进 robot 主界面**（见「第五阶段前端并入」节）；
> composer 保留同样的 selectbox 与研究面板作辅助界面。

### 第一阶段收尾 ✅ 已完成（东汉→中古音类对应表，单提交）

- 新模块 `language/history/eastern_mc_correspondence.py`：
  - `parse_position_description`：`声母[开合][等|重纽AB]韵调` → 六字段（单遍右起，
    每字段至多一次）；3872 条 0 漏网，与 Qieyun 规范位置集逐字段对账 3872/3872。
  - 锚点：703 字（`EASTERN_HAN_DB`，`s2t` 对齐）中 **493 有锚点 / 210 无**
    （`unanchored_characters()` 可查，不回填；人/今/他 只作反切字、使 缺席）。
  - `initial_correspondence()`：30 东汉母→中古声母（初母 1 字无锚定，不在表内）；
    `final_correspondence()`：东汉韵部→中古韵名；合计 **526 条（字,中古位置）对**，
    每对附字表作文字依据，`n<3` 标 `is_exception`。
  - 钉住的散点示例：见母→見51/匣1、匣母→匣24/云13/影2、透母→昌5/透4/徹1、
    阳韵→陽17/唐13/庚8、鱼韵(上)→魚11/麻6/模5/虞2、钟韵→鍾12（1:1）。
- **锚点空间 38 声母 / 58 韵 / 4 调**：CC0 表与 Qieyun 规范集同粒度（双向 missing=[]），
  属上游数据粒度，**不是**《广韵》106 韵分法——文档与报告一律不声称 106 覆盖。
- 报告 CLI：`scripts/correspondence_report.py`（默认完整报告 / `--char` 单字 / `--json`），
  来源（CC0 + blob SHA）与三条局限全部显式打印。
- 性质：对应表是**锚定交集上的观测共现**（非音变规律），模块 docstring 与报告标题均写明。
- 测试：`EasternMcCorrespondenceTests` 21 项（解析器 6 + 覆盖/钉数 11 + 单字查询 2 +
  来源报告 2 + Qieyun 对账 1，Qieyun 缺时跳过）。

### 第四阶段 ① ✅ 已完成（一句话三时期音频对照，单提交）

- 新模块 `language/era_audio.py`：`EraAudio`（key/label/data/kind/status/note/ipa/
  coverage_pct/approx/unknown）+ `make_era_comparison(sentence, middle_system="wangli_mc", ...)`
  → (东汉, 中古, 现代) 三段**各自独立合成**；状态诚实（`ok`/`text_empty`/
  `synth_empty`/`tts_unavailable`），绝不伪造音频；未知 `middle_system` 显式抛 `KeyError`。
- `robot/app.py` `_gen_worker`：三段音频 → **四段**（新增 `reply_mc`，默认王力体系，
  `synthesize_ancient(system_id=...)`）；payload `audios` 新增 `system`/`system_label`/
  `ipa`/`coverage`/`unknown`；`_PHASE_LABEL`/`_PROGRESS` 同步。
- 结果面板新增「三时期对照 · 同一回答」三列（东汉 / 中古 / 现代）：各带独立播放 +
  下载；古韵两列显示 IPA + 覆盖% + 缺字；现代汉语断网显示诚实说明；
  无应答轮次也渲染该节（显示词典未命中说明，不生成对照）。
- 现代汉语段只做真 Edge TTS，断网则该段为空并说明——**不做本地共振峰兜底**（项目契约）。
- 测试：`EraComparisonTests` 3 项（同句「天子」东汉 tʰen vs 王力中古 tʰien、
  现代双分支、text_empty、未知体系 KeyError）+ `WorkerFourAudioTests` 2 项
  （四段 payload / 无应答诚实为空，LLM/TTS/声卡全打桩）；
  `run_feat_tests.py` 110 项全绿，robot app 冒烟 3 项全绿。

### 第四阶段 ② ✅ 已完成（词典未命中接 LLM 翻译，单提交）

- `services/llm_client.py`：
  - `dict_miss_chars(text)`：字级词典覆盖——按出现顺序、去重，返回不出现在
    任何 `TRANSLATION_DICT` key 里的 CJK 字（字级近似，只用于如实标注与触发
    回退，不用于回填）。
  - `_call_translate(...)`：只翻译的调用（`build_translate_prompt` 纯文言输出），
    与 `_call_chat` 同 `trust_env`/超时策略；输出为空或被截断就抛异常，
    绝不把残缺 JSON 当翻译返回。
  - `generate_turn(..., allow_llm_translate=False)` + `_local_fallback(...)`：
    返回新增 `translation_source`（`dictionary` | `llm`）、`missed_chars`、
    `dict_translation`（LLM 补译时保留词典原结果）。
  - **契约**：LLM 只补「翻译」一层，`reply`/`reply_modern` 恒为空——
    「宁可不答不编造」不因 LLM 参与而放宽；开关默认关（opt-in）、
    仅词典模式生效、无密钥/LLM 失败时静默回退词典翻译并如实标注；
    api 模式失败回退时不向同一端点发起第二次 LLM 调用。
  - 顺带修旧 bug：`_call_chat` 非截断失败（断网/401/超时）没有 `break`，
    会加大 max_tokens 无意义地重试一次（旧测试 `assert_called_once` 即被
    违反，此前该测试不在 runner 里所以没暴露）。
- `language/turn_engine.py`：`make_turn(..., allow_llm_translate=False)` 透传，
  `Turn` 新增 `translation_source`。
- `robot/app.py`：对话模式区新增复选框「词典未命中时允许 LLM 辅助翻译」
  （默认 = 是否已有密钥；无密钥时提示不可用）；payload 新增
  `translation_source`/`missed_chars`；元信息行「· 翻译 LLM」；
  翻译行尾「（LLM 补译 · 词典缺 N 字：…）」。
- 旧钉住的 `test_dictionary_miss_returns_no_fabricated_reply` **原样未动**
  （默认关 ⇒ 行为不变）。
- 测试：`run_feat_tests.py` 改为跑两个文件（`test_historical_phonology.py`
  110 + `test_llm_provider.py` 22 = **132 项全绿**）；新增
  `DictMissCharTests` 3 项（`量子计算`→`[量,子,计,算]`、`今天天气真好`→`[]`、
  顺序去重、非 CJK 忽略）+ `DictMissLLMTranslateTests` 7 项（开关/无密钥/
  失败回退/预设应答命中不走 LLM/api 标注/api 失败不二次调用）+
  `DictTranslateCallTests` 2 项（prompt 形态 + 局域网 trust_env、截断抛错）+
  `TurnEngineTranslationSourceTests` 1 项；robot app 冒烟 3 项全绿
  （worker 桩加 `allow_llm_translate` 形参，并断言新 payload 字段）；
  `scripts/smoke_app.py` 6 个 selectbox 正常。

### 第四阶段 ③ ✅ 已完成（多音字词级选音，单提交）

- 新模块 `language/polyphone.py`（jieba 0.42.1 + pypinyin 0.55 + 经验地位映射）：
  - `select_reading(character, context, system_id, word=None)` → `ReadingSelection`
    （character/traditional/system_id/selected/candidates/word/modern_tone/
    tone_class/positions/method/note）。method 五态：`single` / `empirical` /
    `fallback_first` / `suspect_only` / `no_records`。
  - **选音算法（纯经验，IPA 永远来自学者表本身，绝不编造）**：
    1. jieba 对 context 分词，取包含目标字的词（`text_to_ipa` 预切一次逐字映射，
       避免 O(n²)）；
    2. pypinyin（词级多音字消歧，`Style.TONE3`）给现代声调 1–4 → 中古调类
       （1/2→{平}，3→{上,入}，4→{去,入}，`MODERN_TO_TONE_CLASS`）；
    3. 取该字广韵音韵地位（`lookup_qieyun_positions` +
       `parse_position_description`），只保留属该调类的地位；
    4. **经验映射**（每体系懒加载 + lru_cache，`_empirical_votes`）：对同时出现在
       广韵表与学者表中、且学者表恰一条非 suspect 带 IPA 行的「无歧义字」，按
       (地位去声调) → (字,声调,IPA) 投票。确认规则：本调类内投票一致 → 取该值；
       否则全体（任意调）投票一致才取。不一致不产生确认值。
    5. 确认值须与该字非 suspect 行中**恰好一个** distinct IPA 相等 → 选中该行
       （`empirical`）；
    6. 否则不可判定 → 首条非 suspect 行（`fallback_first`），note 逐条写明卡因
       （声调不可判定 / 广韵无属该调类地位 / 无一致读法 / 一致读法与各行均不符），
       **不猜测**。
  - 依赖缺失诚实降级：无 jieba→逐字 + 标注；无 pypinyin→声调不可判定直接
    fallback；无 opencc→繁简退化为原字。
- `language/ancient_tts.py`：
  - `text_to_ipa(classical, system_id=None, context=None)`：学者体系下逐字改走
    `select_reading`；新增 `context` 形参（缺省用 classical 自身）。
  - `AncientResult.selections: tuple`（默认 `()`）：多音字选音明细
    `(字, IPA 或 None, method, note)`，仅 ≥2 条非 suspect 行时出现。
  - **旧路径（legacy）与单行字行为完全不变**（已钉测试全绿）。
- **实测钉住的案例（wangli_mc 除非另注）**：
  - `empirical`：解(解说)→`kai`（見開佳上，同类字佳/懈一致读）、土(率土)→`tʰu`
    （透模上）、好(好人)→`hɑu`（曉豪上，蒿一致读）、行(行走, **karlgren_mc**)→`ɣɐŋ`
    （匣開二庚平，杏一致读）。
  - `fallback_first`：行(银行/行走, wangli)→`ɣɑŋ`（庚类投票不一致 杏ɣɐŋ/垎ɣɐk）、
    中(中国/打中)→`ȶǐuŋ`（一致读 ȶǐuk 与各行 ȶǐuŋ 不符）、率(率领)→`ʃwi`
    （无投票字）、好(喜好)→`hɑu`（广韵只有豪上，无去/入地位）。
  - `single`：東→`tuŋ`、银(简)→`ŋǐěn`（s2t 查 銀，显示原字）。
  - `no_records`：龘。
- **依赖坑（新）**：
  1. **jieba 0.42.1** 装在 `.libs_guyun\jieba`。PyPI 镜像上的 `jieba==0.21` 是
     Python 2 毒包，**勿装**；0.42.1 用 sdist 手工解压（无 setuptools，不能 pip
     build）。首次 `jieba.cut` 建词表 ~0.3–1s（缓存在 `Temp\jieba.cache`）。
  2. **pypinyin 0.55.0 API 已改名**：`from pypinyin import pinyin, Style`
     （旧函数名 `pypinyin` 已不存在，import 会 `ImportError`）；`pinyin(word,
     style=Style.TONE3)` 返回逐字 list-of-lists，声调为结尾数字。
- 测试：`PolyphoneSelectionTests` 22 项（基础 6 + empirical 4 + fallback 5 +
  映射/接线 7）；`run_feat_tests.py` **154 项全绿**（132+22）；robot 冒烟 3 项全绿；
  `scripts/smoke_app.py` 6 个 selectbox 正常。

### 逐音素合成验证报告 ✅ 已完成（2026-11-03，`804db34` + `0e8ce5e`）

- 评审要求：**「有音频输出」≠成功**——引擎会静默丢弃或替换个别音素。
  `scripts/phoneme_verification_report.py`（只读、可重跑）对 11 家学者体系 +
  legacy 703 字表，按冻结探针矩阵聚合逐音素 eSpeak/formant 能力，并对
  12 句公有领域文言跑生产 `text_to_ipa` 选音路径，产出：
  - `docs/reports/phoneme_verification/REPORT.md`（逐体系级别分布
    full/approx/partial/untested/silent + 逐音素丢失矩阵含示例字）；
  - `polyphone_verification.csv`（**185 行**：37 `empirical` = 当前数据规则下的
    **经验性选择，非学者确认**；148 `fallback_first` 逐行写明卡因；
    末尾两列空列预留人工核验）；`summary.json`（机器可读统计）；
  - 完整候选表 72,045 行约 5MB 可重跑再生 → **gitignore 不入库**。
- 关键数字：`lifanggui_oc` 100% full（11160/11160、0 缺字、0 silent）；
  全部体系 untested=0 / silent=0（冻结矩阵覆盖全部符号）；wangli_mc
  partial 4433 读法 = 7 个不可发音声母（ɣ/ȶ/tʃ/ȡ/ʃ/ɽ/dʒ），每读法恰丢 1 token；
  approx（如 `̌` 组合长音符号）只保证「有声」，不保证听感正确。
- 顺带修复（`0e8ce5e`）：`text_to_ipa(context=...)` 中 `context≠classical`
  时 word_at 按字位映射到 context 同位词（借错词声调；字不在 context 时
  变「词中找不到目标字」）。现改按「该字在 context 中首次出现所在的词」
  （与 `word_tone` 隐式路径同口径），字不在 context 回退单字常读；
  `context==classical`（含缺省）与 legacy 行为不变，+2 项回归测试钉住。
- Windows 回归（本分支动过 robot/app.py、services/llm_client.py、
  language/turn_engine.py）：`run_feat_tests.py` **156 项全绿**
  （134 音韵 + 22 LLM；断网 LLM 回退日志为预期）、
  `tests/test_robot_app_smoke.py` 3/3、`scripts/smoke_app.py` EXIT=0
  （6 个 selectbox）。**Jetson 真机链路本机无法运行**；且 2026-11-03
  用户决定 **v5 优先面向 Windows 用户**（v5-goal.md 顶部有记录），
  Jetson 真机回归已降为可选项、不再是 v5 完成判据。

### 第五阶段前端并入 ✅ 已完成（2026-11-03，robot = v5 主界面）

用户实测反馈定调：**「v5 应该是在 v4 的基础上做开发」**——v4 是 Windows 机器人
界面（`robot/app.py`），composer（`guyun_app.py`）是 v3 界面。此前 v5 能力
（第三阶段 ③ 学者体系 UI、研究面板）落在 composer、部分落在 robot → 全部并入 robot：

- **拟音体系 selectbox**（左列，仅古韵模式显示）：默认「东汉洛阳官音（默认）」
  （`system_id=None` → legacy 路径，行为与 v4 完全一致），另 11 套 Sinica 学者
  体系（上古 5 / 中古 6，标签来自 `SCHOLAR_SYSTEMS_ALL`）；自然语音模式强制
  `system_id=None`（选中值忽略）。
- **Worker**（`_gen_worker`）：`cfg["system_id"]` 决定 user / reply_anc 的
  `synthesize_ancient(system_id=...)`（学者路径缺字计 unknown，**不补现代拼音**）。
  **中古槽自动避让**：主体系与中古槽默认（王力中古）重合时，中古槽自动改用
  董同龢中古并给 `middle_note`（界面上 caption 提示）；其他体系保持对王力中古
  的三时期对照。
- **逐字双列数据**：`AncientResult.characters`（收录 / 拼音近似 /
  缺字（不补拼音））× `phoneme_capability.assess_ipa` 引擎侧能力 → payload
  `scholar_rows`（char/ipa/status/cap）/ `scholar_counts` / `scholar_selections`
  （多音字选音 4 元组）；结果面板学者路径渲染逐字对照表 + 引擎侧能力汇总 +
  选音依据表；无体系（legacy）路径保持原逐字表。
- **结果区**：IPA 块改用 worker 给出的所选体系逐字 IPA（不重算；旧版结果兜底
  本地查表）；三时期对照首列改用 worker 的 reply_anc 数据（IPA/覆盖/缺字随所选
  体系，标题「所选体系」）；音频卡片标题、meta 行随体系名动态化；`reply_anc`
  音频 dict 新增 `system`/`system_label`/`ipa`/`coverage`/`approx`/`unknown`。
- **研究面板**（右栏末尾新函数 `_render_phonology_research()`，自 composer 原样
  移植）：🧭 历史音系探索（广韵音韵地位 / PHONO-ML / 中原音韵 / lookup_reading）/
  🔀 同字跨体系对照（争议项 + 各体系覆盖）/ 🏛️ Sinica CCR 原始记录检索
  （数据包缺失时显示 unzip 指引）。全部离线数据、来源可溯。
- **热重载**：`_RELOAD_ORDER` 增补 `language.history.*` 子模块 +
  `language.polyphone`/`phoneme_capability`/`era_audio`（缺失模块安全跳过）。
- **测试**：`run_feat_tests.py` 改为跑 3 个文件 = **161 项全绿**（134 音韵 +
  22 LLM + 5 robot 冒烟：基础渲染 / 古韵模式 selectbox+研究面板渲染 / 四段音频
  payload / 无应答诚实为空（新增 v5 键缺省断言）/ **wangli_mc 学者路径**
  （真合成 + `scholar_rows` 键齐整 + 缺字 ipa=None + 中古槽避让断言
  `"自动改用" in middle_note` + `reply_mc.system == "dongtonghe_mc"`））。
  ⚠️ 避让提示文案是「中古槽**自动改用**」（不是「自动换」）。
  `scripts/smoke_app.py`（composer）6 个 selectbox 仍正常。
- **composer 去留（待用户拍板）**：composer 保留同样的拟音体系 selectbox 与
  三个研究面板作为辅助界面（冒烟仍过）；**v5 主界面 = robot**。
- v4 便携打包（`packaging/` `launcher_v4` + PyInstaller）本就基于 robot 界面，
  改动后**可直接重新打包**出 v5 便携版（用户未要求，先不动）。

验证：`run_feat_tests.py` 161 OK（exit 0）；`scripts/smoke_app.py` EXIT=0；
:8502 重启（`STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false` + 全量 PYTHONPATH +
CWD=worktree，日志 `.robot_server.log`）HTTP 200、无 Traceback。

### 声音合成修复（2026-11-03，用户报告「有的字正常、有的像退回共振峰」）

**诊断结论（日志可证）**：用户会话期间 robot :8502（13:51–14:00 渲染 9 次）
与 composer :8501（12:39/13:50 渲染 3 次）的日志里**零条**
`[sound_synth] eSpeak-ng error:` → 按句共振峰兜底**从未触发**。
听感差异的真实原因：eSpeak-ng 1.52 `-v zh` 对 28 个实测符号（ȶ ȡ ɣ ʃ ɽ
dʒ tʃ ɡ ɪ …，冻结清单见 `tests/test_historical_phonology.py::test_frozen_silent_symbols`）
**整段静默丢弃**——如 行→ɣɑŋ 丢 ɣ、中→ȶǐuŋ 丢 ȶ，音节听起来「缺一段」。
跨体系对照（东汉 legacy 干净 vs 学者体系缺声母）即可复现，UI 逐字表已注明「丢 X」。

**已修（本次提交）**：

1. `sound_synth.synth_with_espeak`：临时 wav 不再用 `%TEMP%`——沙箱化进程树里
   原生子进程 espeak.exe 只能写工作区内（写 %TEMP% 报 `Can't write to` 且
   **退出码仍为 0**，`check=True` 抓不到）。新增 `_espeak_wav_path()`：优先
   `<应用目录>/.tmp_espeak/`（`tempfile.mkstemp`），不可写才退回系统临时目录；
   去掉 `check=True`，rc≠0 → RuntimeError；并验证输出文件存在、size>0、
   RIFF 头，任何失败走原 `except → print → None`（整句回退共振峰，但现在
   **必然留日志**，不再是静默空音）。
2. 共振峰引擎元音表：补 `ɪ`；新增 `PRECOMPOSED_VOWEL_BASE`（约 50 个带调
   元音 → 基础键）——语料实测预组合带调元音共约 5000 处（李方桂中古表
   â=3256 ă=697 ï=675 ĕ=343，东同龢 2 处），旧表无条目 → 回退引擎对这些
   元音**完全不发声**。`is_vowel` / formant 查找改走 `_vowel_base()`。
   分解型（王力 i+U+030C 等，caron 29573 处为主）不受影响（基础元音原本就在表内）。
3. `robot/app.py` + `guyun_app.py`（composer v3）：覆盖率表「缺陷行 / 空韻母 /
   韻部数 / 備註行 / 零声母行」列 scholar 行是 int、其他行是 `"—"` →
   `pyarrow.lib.ArrowTypeError: Expected bytes, got a 'int' object`（两应用日志均现：
   robot 9 次、composer 3 次，Streamlit 吞掉后表格渲染缺列）→ `st.dataframe`
   前统一 str 化。

**测试**：`run_feat_tests.py` 161 → **168 项全绿**。新增 7 项
（`SoundSynthEngineRobustnessTests`）：临时路径在应用目录内；rc=0+无文件 → None；
rc=0+0 字节 → None；rc≠0 → None；rc=0+有效 RIFF → 返回音频；预组合带调元音
â ă ï ĕ ǐ ǔ 共振峰全部发声；ɪ 发声。`test_formant_status_uses_real_engine_sets`
的 ɪ pin 由 SILENT → OK（已进元音表，防漂移 pin 同步更新）。

**文档**：`v5-goal.md` 日期归一化（2026-11-05 → 2026-11-03 两处）。

### 共振峰建模 + 逐词路由（2026-11-03，用户要求「你给它们建模不行吗」，已批准）

此前 eSpeak 静默丢弃的 13 个 IPA 符号（ȶ ȡ ɖ ɟ ɡ ɳ ɱ ɲ ɽ ʈ ʅ ʎ ç）在
共振峰兜底的 `CONSONANT_PARAMS` 里也缺失——含这些音素的词即使路由到
兜底引擎，缺段**照样缺**，兜底形同虚设。现已补上：

1. **`CONSONANT_PARAMS` 新增 17 条**：上述 13 个 IPA 辅音（塞音/擦音/鼻音/
   流音参数按发音部位方式建模）+ 4 个双字塞擦音 tɕʰ/tʂʰ/tsʰ/dʐ（这 4 个
   在分音器列表里、参数表漏建，旧代码对 q/ch/c 把整条塞擦音静默丢弃
   ——顺带修复的潜伏 bug）。
2. **`FORMANT_CHAR_ALIAS`**：7 个带附加符的数据质量符号（ḍ ṭ ṇ ṣ ẓ ś ź）
   按 IPA 附加符约定解码（点下=卷舌系列、锐音符=硬腭塞擦/擦音），
   ậ → a（李方桂表残留）。**仅合成侧解码**——读音数据不动，eSpeak 侧
   报告（SILENT_FROZEN / dropped_symbols / 能力档）完全不变。
3. **`synthesize_text` 逐词路由**：短语内只要有一个词含 eSpeak 实测
   静默丢弃音素，该短语改逐词路由——干净词仍连续打包 eSpeak（保留
   内部韵律），被丢音素的词逐个走共振峰；eSpeak 整组失败时该组降级
   逐词共振峰。
4. **UI**：robot/composer 逐字表丢段标注补「，转共振峰」（含被丢音段的
   词整词转共振峰，音段不再缺，音色不同）；composer 帮助行同步改写。
5. **能力报告**：`_formant_status` 同样解码 alias 再查参数表 → 各体系
   `system_capability_report` 的 formant_full/formant_partial 活算数字
   整体变化（eSpeak 侧数字冻结不变）；`test_formant_status_uses_real_engine_sets`
   的 ɡ/ȶ pin 由 SILENT → OK。

**验证**：`run_feat_tests.py` 168 → **174 项全绿**（+6：alias 解码、17 条
新建参数长度确定性、路由谓词、逐词路由行为 3 条——干净词打包 / 静默词
转共振峰 / 两引擎间停顿）。活体冒烟：`synthesize_text('tɕiɛn ɣɑŋ')` →
eSpeak "tɕiɛn" 21503 采样点 + 共振峰 "ɣɑŋ" 6614 采样点（0.30s，
ɣ+ɑ+ŋ 三段全部发声），无缺段。

提交 30df75a。

### eSpeak 近似层（2026-11-03，用户反馈「共振峰太机械了，能不能让 espeak 可以读出这些字」）

`-x` 音素转储复核推翻了两条旧结论：

1. **28 个 SILENT_FROZEN 符号并非无声**：27 个被 eSpeak 替换成声门塞音
   `[ʔ]`（`-x` 转储为 `?`，凭空造出数据里不存在的音段），仅 `ɡ` 真静默。
2. **旧 `ESPEAK_IPA_MAP` 有 7 个值在生产上早已毁音**：`O/V/7/{`（ɔ ɐ ɤ æ）
   在 zh 声音下不产任何音素（整音节 ~0.43 s 静音），`s`/`z``（ʂ ʐ）的反引号
   是 [[ipa]] 语法里的重音符，**截断 IPA 段**——「ʂɑŋ」旧值只读出一个 "s"。

改动（单提交 `63271d2`，可整段回退）：

1. **`ESPEAK_IPA_MAP` 修 7 值**（值变、键集不变）：ɔ→o ɐ→a æ→a ʌ→a ɤ→a
   ʂ→S ʐ→Z。全部 24 个不同值逐一 `-x` 验证产出真实音素（`.probe_mapvalues.txt`）。
2. **新增 `ESPEAK_APPROX_MAP`**（28 键，合成侧近似层，与 `FORMANT_CHAR_ALIAS`
   同级——决定"怎么读出来"，数据与矩阵不动）：ȶ/ȡ→ts，ʈ/ṭ→t，ɖ/ɽ/ḍ→r，
   ɳ/ṇ→n，ɱ→m，ɲ→J，ɟ/ʎ→j，ɣ→x，ʃ/ʅ/ç/ś/ṣ→S，ʒ/ź/ẓ→Z，ɡ→g，ɪ→i，
   元音带符（ä å ậ）→a。每个值 `-x` 验证：无 `?`、无截断、`A` 音节完整。
   值集**禁止**反引号与大写 I/U/O/Y/V（zh 声音吞字符）。
3. **`sound_synth._espeak_approx`**：`synth_with_espeak` 管线在 `preprocess_ipa`
   之后应用近似层（两表键集不相交，顺序不影响结果）。
4. **路由降级为防御性**：`_word_dropped_by_espeak` 改为「SILENT **且**近似层
   未覆盖」才转共振峰（当前 28 全覆盖 → 恒 False）；全部词默认走 eSpeak，
   共振峰仅在近似层缺键或 eSpeak 整组硬失败时触发。
5. **UI/报告措辞**：丢段标注「，转共振峰」→「，eSpeak 近似读」；caption/
   验证报告 partial 档改写（如实：多数被替换成 [ʔ]、个别整段丢失，朗读按
   近似音替代）。
6. **诚实性（宁缺毋滥）**：`classify_symbol` / `SILENT_FROZEN` / 能力矩阵
   **保持如实**——28 个符号仍报 SILENT（冻结测试原样通过）；近似是引擎侧
   解码，不加进 `ESPEAK_IPA_MAP` 键集（否则 classify_symbol 会翻成 OK，
   破坏冻结契约）。

**验证**：`run_feat_tests.py` 174 → **179 项全绿**（+5：近似层全覆盖、
近似值逐值 `-x` 实测、修复值逐值 `-x` 实测、近似词留 eSpeak 路由、
生产词形音长钉住）。冒烟：`synthesize_text('tɕiɛn ɣɑŋ')` 单次 eSpeak 调用
（无共振峰）；`ɣɑŋ` 18990 采样（旧 `?A55N` 17572，ʔ 不占时长）、`ʂɑŋ`
19141（旧 `s_|` 12479 截断）、`ʐɑŋ` 18418、`tʂʰɑŋ` 21354、`ɔŋ` 16419
（旧 9503 静默）、`ɪ` 14521（旧 `?_|` 10967）。28 符号逐一 `X+ɑ` 全部可出声。

### 下一阶段（第四阶段余下，用户已定顺序）

- ✅ ① 一句话多时期音频对照（东汉 / 中古 / 现代同句三版）——已完成；
- ✅ ② 翻译层词典未命中时接 LLM（宁可不答不编造，标注 dict vs LLM）——已完成；
- ✅ ③ 多音字按词切分选音——已完成（jieba + pypinyin + 经验地位映射，见上）；
- ✅ **第五阶段前端并入**：v5 全部能力（拟音体系 selectbox / 逐字双列 /
  研究面板）落到 v4 robot 界面（2026-11-03，见上节）；
- ~~Jetson 真机链路回归清单~~（2026-11-03 起 **降为可选**：v5 优先面向
  Windows 用户，Jetson 不再是 v5 完成判据；有真机窗口时再按 v5-goal.md
  第五阶段清单执行）。

## 四、已验证可用的能力（2026-10-30 实测）

| 能力 | 状态 |
|---|---|
| 白话→古文（词典，缺字如实标注） | ✅ `dict_miss_chars` 字级覆盖 |
| 词典未命中 LLM 补译（opt-in，标注来源） | ✅ `allow_llm_translate`，回答恒不编造 |
| 东汉音 IPA（703 字，legacy 路径） | ✅ |
| 11 家学者拟音逐字合成 | ✅ eSpeak 出声，双列对照 UI |
| 多音字词级选音（学者体系，标注 dict vs 经验回退） | ✅ `language/polyphone.py`，empirical/fallback_first 双态 + 卡因说明 |
| 逐音素合成验证报告（逐音素级别 + 多音字核验集） | ✅ `scripts/phoneme_verification_report.py`，185 行核验集（empirical 为经验性选择，非学者确认） |
| 东汉→中古音类对应表 | ✅ 493/703 锚定，526 对，30 母/58 韵粒度，`scripts/correspondence_report.py` |
| 古韵合成 eSpeak | ✅ 32540 采样点 / 1.48s |
| Edge TTS 现代朗读 | ✅ MP3 |
| 三时期音频对照（东汉 / 中古王力 / 现代） | ✅ `language/era_audio.py`，robot 面板三列 |
| v5 拟音体系 + 逐字双列 + 研究面板（robot 主界面） | ✅ `robot/app.py`（第五阶段前端并入，2026-11-03），run_feat_tests 174 项全绿 |
| eSpeak 沙箱兼容（临时文件在应用目录 + rc=0 空文件/RIFF 检测） | ✅ `sound_synth._espeak_wav_path` + 输出校验 |
| 共振峰回退引擎完整度（ɪ + 预组合带调元音 â ă ï ĕ 等发声） | ✅ `sound_synth.PRECOMPOSED_VOWEL_BASE` / `VOWEL_FORMANTS` |
| 缺段词整词可出声（13 IPA 符号 + 4 双字塞擦音建模 + 逐词路由 + 附加符解码） | ✅ `sound_synth.CONSONANT_PARAMS` / `FORMANT_CHAR_ALIAS` / `_routed_phrase`（2026-11-03） |
| 切韵对照（Qieyun） | ✅（依赖坑 2 的 networkx 补丁） |
| 录音 + 回放 | ✅ selftest True |
| 语音识别 | ✅ SenseVoice 逐字正确；Vosk 兜底可用 |
| 文言对谈 API | ✅ 8/8 成功（推理模型 token 已修） |
| 设备播放 | ✅ 5 个输出设备 |

模型已下好在 `.wt-feat-phon/models/`（sense-voice 229 MB、vosk-small-cn 65 MB），
`models/` 与 `espeak-ng/` 都被 gitignore，换机器要重跑
`python scripts/download_models.py`（支持断点续传）。

## 五、工作节奏约定

- 每完成一块就单独提交，提交信息写清「为什么」而非「改了什么」
- 涉及数据时，宁可报「缺」也不编造（这是本项目的既有契约）
- 文档与代码要同步改：`docs/v5-goal.md` 的状态表、`docs/HISTORICAL_PHONOLOGY_ARCHITECTURE.md`
- **推送**：分支已与 origin 同步（2026-10-31）；本机无保存凭据，需要推送时
  让用户提供临时 PAT，一次性 URL 方式推送，**不写入 config、用完提醒吊销**；
  不要动 `main` 检出的根工作树
