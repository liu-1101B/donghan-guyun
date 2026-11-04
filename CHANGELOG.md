# 变更记录

## v4.1.0 — 2026-11-04

v4 行的热修复版：把 11/04 QA 发现的四个问题修掉，**不含 v5 任何新功能**
（研究面板、`language/history/`、学者音色等都不在这版里）。

### 修复

- **[严重] 简繁同字不同音**：东汉官音旧表以简体为键，繁体输入（如「東」）精确查不到，
  就落进拼音近似层，界面音标与合成读音分叉。现查表字形无关
  （`phonology_db.lookup_char_invariant`：原字 → 繁转简 → 简转繁，懒加载
  `language/polyphone.py` 的 opencc 转换，opencc 缺失时退化为精确匹配、不崩溃）：
  「東」按「东」读 tuŋ、「龍」按「龙」读 ljoŋ；两种字形都没收录的字（如「很」）
  仍如实走拼音近似，不伪造数据。
- **翻译逐字音标与韵部**：「我的话·古汉语」的翻译现在同样逐字列出音标
  （与回答共用 `analyze_reply`）；legacy 逐字表新增「韵」列
  （字｜东汉 IPA｜韵｜声调｜来源），如「东韵」「钟韵」。
- **翻译音频卡带逐字 IPA**：用户音频卡与回答古音卡同口径展示。
- **大模型静默回退**：选了 API 但调用失败/未配密钥时，界面顶部 `st.warning`
  提示原因（`llm_note`），不再悄悄回退到本地词典。

### 测试与打包

- 回归测试 `tests/test_v410_release_fixes.py`（15 项），全量 42 项通过。
- 便携包：`guyun-robot-v4.1.0-windows-x64.zip`（约 237 MB，免安装，
  另附一键下载识别模型的 bat）。

## v4.0.0 — 2026-10-29

Windows 上把新版机器人界面做成可用、可分发的一版。

### 新增

- **Windows 原生音频后端**（`robot/windows_audio.py`）：sounddevice/PortAudio，不再依赖 `arecord`/`pw-play`/`wpctl`。
  Linux/Jetson 仍走原 PipeWire/ALSA 路径。
- **按住说话**：自建 Streamlit 组件 `components/hold_to_record/`，浏览器侧采 PCM、松手编码成 WAV 回传，
  本机识别后回填输入框。取代固定 5 秒的服务端录音。
- **界面内填 API**：左侧「大模型 API 设置」直接写本机 `.env` 并立即生效，不用改文件、不用重启。
- **识别引擎换 SenseVoice**（sherpa-onnx，228 MB 模型）：带标点，中文准确率明显高于 Vosk 小模型；
  后端按可用性自动选择 `SenseVoice > Paraformer > Vosk`。
- 单元测试 27 项（音频适配、设备列表、LLM 两条路径、后端选择、界面冒烟）。

### 修复

- 深色模式下「对话模式 / 语音模式」等标签看不清：主题固定为浅色宣纸（`.streamlit/config.toml`），
  CSS 显式给 `.stApp` 上墨色。
- 播放设备下拉列出 31 条重复项（同一设备被 MME/DirectSound/WASAPI/WDM-KS 各列一次）→ 去重后 22 条，
  蓝牙名清洗成「设备名（蓝牙·免提）」，同名端点带 ` · #序号`。
- 选了具体输出设备，提示却写「已朗读到默认输出设备」→ 如实报设备名。
- 语音识别结果回填失败（用户编辑过输入框后，前端值会覆盖服务端赋值）→ 换版本化控件 key。
- 录音松手在按钮外触发时永久卡在录音态 → 事件改绑 document + 超时兜底。
- 打包版误报「识别模型未安装」（判断写死 `vosk-small-cn`）→ 改为后端探测。
- `ROBOT_README` 里残留的「本地大模型 127.0.0.1:8080」已删除（该路线已不存在）。

### 变更

- 仓库整理：文档归入 `docs/`，开发脚本归入 `tools/`，`packaging/` 不再复制一份源码（v3 的
  PyInstaller + Inno Setup 脚本已移除，需要时从 git 历史取）。
- README 的「快速开始」改为指向 v4 便携包（原来那个 Releases 链接是死链）。

### 分发

- 便携包：`guyun-robot-v4.0.0-windows-x64.zip`（约 188 MB，免安装，另附一键下载识别模型的 bat）。

## v3.0.0 — 2026-07-20

- 首个可分发版本：独立合成器界面 `guyun_app.py` + PyInstaller/Inno Setup 安装包，
  703 字东汉音韵库、eSpeak-ng + 共振峰双引擎、Edge-TTS 现代朗读。
