# 跨体系同字碰撞表（原始 IPA → 近似 IPA → 真实音频）

- 生成: `scripts/qa_pronunciation_audit.py collision`，2026-11-01
- 字集: 55 字（37 审核字 + 18 高频字），体系: 东汉(legacy) + 6 中古体系
- 音频引擎: C:\Users\HP\Documents\deepseek-harness\default-workspace\donghan-guyin\.wt-feat-phon\espeak-ng\espeak-ng.exe
- 每格 = 该体系首个非 suspect 行的 IPA；括号内为该字在此体系的不同读数个数
- 时长 = 真实 eSpeak 合成样本数换算（含 80ms 词间留白），同一引擎内可横向比较

| 字 | 王力系統 | 董同龢系統 | 周法高系統 | 李方桂系統 | 陳新雄系統 | 高本漢系統 | 东汉(legacy) |
|---|---|---|---|---|---|---|---|
| **行** | `ɣɑŋ`→`xAN` (×2) [861ms] | `ɣɑŋ`→`xAN` (×2) [861ms] | `ɣɑn`→`xAn` (×3) [847ms] | `ɣâng`→`xâng` (×2) [918ms] | `ɣɑŋ`→`xAN` (×2) [861ms] | `ɣɑŋ`→`xAN` (×2) [861ms] | `ɦaŋ`→`haN` [832ms] |
| **重** | `ȡǐwoŋ`→`tsǐwoN` [1189ms] | `ȡʰjuoŋ`→`tshjuoN` [986ms] | `ɖiuoŋ`→`riuoN` [994ms] | `ḍjwong`→`rjwong` [900ms] | `ȡʰǐuŋ`→`tshǐuN` [1131ms] | `ȡʰi̯woŋ`→`tshi̯woN` [1210ms] | `droŋ`→`droN` [794ms] |
| **樂** | `ŋau`→`Nau` (×3) [911ms] | `ŋau`→`Nau` (×3) [911ms] | `ŋau`→`Nau` (×3) [911ms] | `ngau`→`ngau` (×3) [991ms] | `ŋɔu`→`Nou` (×3) [756ms] | `ŋau`→`Nau` (×3) [911ms] | — |
| **長** | `ȡǐaŋ`→`tsǐaN` (×2) [1110ms] | `ȡʰjɑŋ`→`tshjAN` (×2) [973ms] | `ɖiɑŋ`→`riAN` (×2) [809ms] | `ḍjang`→`rjang` (×2) [926ms] | `ȡʰǐɑŋ`→`tshǐAN` (×2) [1131ms] | `ȡʰi̯aŋ`→`tshi̯aN` (×2) [1131ms] | — |
| **得** | `tək`→`t@k` [730ms] | `tək`→`t@k` [730ms] | `tək`→`t@k` [730ms] | `tək`→`t@k` [730ms] | `tək`→`t@k` [730ms] | `tək`→`t@k` [730ms] | — |
| **說** | `ɕǐwɛi`→`SǐwEi` (×3) [1256ms] | `ɕjuæi`→`Sjuai` (×3) [917ms] | `ɕiuæi`→`Siuai` (×3) [1039ms] | `śjwäi`→`Sjwäi` (×3) [1144ms] | `ɕǐuɛi`→`SǐuEi` (×3) [1348ms] | `ɕi̯wɛi`→`Si̯wEi` (×2) [1256ms] | — |
| **為** | `ɣǐwe`→`xǐwe` [1036ms] | `ɣjuĕ`→`xjuĕ` [991ms] | `jiue`→`jiue` [994ms] | `jwĕ`→`jwĕ` [779ms] | `jǐuɛ`→`jǐuE` [1118ms] | `jwie̯`→`jwie̯` [950ms] | — |
| **華** | `ɣwa`→`xwa` (×2) [842ms] | `ɣua`→`xua` (×2) [775ms] | `ɣua`→`xua` (×2) [775ms] | `ɣwa`→`xwa` (×2) [842ms] | `ɣua`→`xua` (×2) [775ms] | `ɣwa`→`xwa` [842ms] | — |
| **率** | `ʃwi`→`Swi` (×2) [849ms] | `ʃjuei`→`Sjuei` (×2) [833ms] | `ʂiuɪi`→`Siuii` (×2) [1282ms] | `ṣjwi`→`Sjwi` (×2) [922ms] | `ʃǐue`→`Sǐue` [1120ms] | `ʂwi`→`Swi` (×2) [849ms] | — |
| **王** | `ɣǐwaŋ`→`xǐwaN` [1178ms] | `ɣjuɑŋ`→`xjuAN` [911ms] | `jiuɑŋ`→`jiuAN` [965ms] | `jwang`→`jwang` [940ms] | `jǐuɑŋ`→`jǐuAN` [1032ms] | `ji̯waŋ`→`ji̯waN` [1112ms] | `ɦʷaŋ`→`hwaN` [858ms] |
| **朝** | `ȶǐɛu`→`tsǐEu` (×2) [1209ms] | `ȶjæu`→`tsjau` (×2) [1037ms] | `ʈiæu`→`tiau` (×2) [1053ms] | `ṭjäu`→`tjäu` (×2) [1014ms] | `ȶǐɛu`→`tsǐEu` (×2) [1209ms] | `ȶi̯ɛu`→`tsi̯Eu` (×2) [1209ms] | `trjaw`→`trjaw` [921ms] |
| **中** | `ȶǐuŋ`→`tsǐuN` [1110ms] | `ȶjuŋ`→`tsjuN` [936ms] | `ʈiuŋ`→`tiuN` [982ms] | `ṭjung`→`tjung` [932ms] | `ȶǐoŋ`→`tsǐoN` [1110ms] | `ȶi̯uŋ`→`tsi̯uN` [1110ms] | `truŋ`→`truN` [830ms] |
| **道** | `dɑu`→`dAu` [689ms] | `dʰɑu`→`dhAu` [771ms] | `dɑu`→`dAu` [689ms] | `dâu`→`dâu` [847ms] | `dʰɑu`→`dhAu` [771ms] | `dʰɑu`→`dhAu` [771ms] | `duʔ`→`du?` [727ms] |
| **難** | `nɑn`→`nAn` [795ms] | `nɑn`→`nAn` [795ms] | `nɑn`→`nAn` [795ms] | `nân`→`nân` [795ms] | `nɑn`→`nAn` [795ms] | `nɑn`→`nAn` [795ms] | — |
| **好** | `hɑu`→`hAu` [746ms] | `xɑu`→`xAu` [775ms] | `xɑu`→`xAu` [775ms] | `xâu`→`xâu` [947ms] | `xɑu`→`xAu` [775ms] | `xɑu`→`xAu` [775ms] | `huʔ`→`hu?` [791ms] |
| **發** | `pǐwɐt`→`pǐwat` [1067ms] | `pjuɐt`→`pjuat` [828ms] | `piɑt`→`piAt` [764ms] | `pjwɐt`→`pjwat` [903ms] | `pfǐuɐt`→`pfǐuat` [1105ms] | `pi̯wɐt`→`pi̯wat` [1067ms] | — |
| **覺** | `kau`→`kau` (×2) [892ms] | `kau`→`kau` (×2) [892ms] | `kau`→`kau` (×2) [892ms] | `kau`→`kau` (×2) [892ms] | `kɔu`→`kou` (×2) [721ms] | `kau`→`kau` (×2) [892ms] | — |
| **空** | `kʰuŋ`→`khuN` [856ms] | `kʰuŋ`→`khuN` [856ms] | `kʰuŋ`→`khuN` [856ms] | `khung`→`khung` [926ms] | `kʰoŋ`→`khoN` [856ms] | `kʰuŋ`→`khuN` [856ms] | `kʰuŋ`→`khuN` [856ms] |
| **曲** | `kʰǐwok`→`khǐwok` [1121ms] | `kʰjuok`→`khjuok` [882ms] | `kʰiuok`→`khiuok` [1003ms] | `khjwok`→`khjwok` [957ms] | `kʰǐuk`→`khǐuk` [1055ms] | `kʰi̯wok`→`khi̯wok` [1121ms] | — |
| **血** | `hiwet`→`hiwet` [946ms] | `xiuɛt`→`xiuEt` [1141ms] | `xiuɛt`→`xiuEt` [1141ms] | `xiwet`→`xiwet` [986ms] | `xiuet`→`xiuet` [1098ms] | `xiwet`→`xiwet` [986ms] | — |
| **稱** | `tɕʰǐəŋ`→`tShǐ@N` [1167ms] | `tɕʰjəŋ`→`tShj@N` [1023ms] | `tɕʰiɪŋ`→`tShiiN` (×2) [1129ms] | `tśhjəng`→`tShj@ng` [1094ms] | `tɕʰǐəŋ`→`tShǐ@N` [1167ms] | `tɕʰi̯əŋ`→`tShi̯@N` [1167ms] | — |
| **數** | `ʃǐu`→`Sǐu` (×3) [1020ms] | `ʃjuo`→`Sjuo` (×3) [848ms] | `ʂiuo`→`Siuo` (×3) [968ms] | `ṣju`→`Sju` (×3) [833ms] | `ʃǐu`→`Sǐu` (×3) [1020ms] | `ʂi̯u`→`Si̯u` (×2) [1020ms] | — |
| **落** | `lɑk`→`lAk` [756ms] | `lɑk`→`lAk` [756ms] | `lɑk`→`lAk` [756ms] | `lâk`→`lâk` [756ms] | `lɑk`→`lAk` [756ms] | `lɑk`→`lAk` [756ms] | — |
| **種** | `tɕǐwoŋ`→`tSǐwoN` [1164ms] | `tɕjuoŋ`→`tSjuoN` [940ms] | `tɕiuoŋ`→`tSiuoN` [1046ms] | `tśjwong`→`tSjwong` [985ms] | `tɕǐuŋ`→`tSǐuN` [1084ms] | `tɕi̯woŋ`→`tSi̯woN` [1164ms] | — |
| **都** | `tu`→`tu` [711ms] | `tuo`→`tuo` [725ms] | `tuo`→`tuo` [725ms] | `tuo`→`tuo` [725ms] | `tu`→`tu` [711ms] | `tuo`→`tuo` [725ms] | `ta`→`ta` [711ms] |
| **還** | `ɣwan`→`xwan` (×2) [911ms] | `ɣuan`→`xuan` (×2) [847ms] | `ɣuan`→`xuan` (×2) [847ms] | `ɣwan`→`xwan` (×2) [911ms] | `ɣuan`→`xuan` (×2) [847ms] | `ɣuan`→`xuan` (×2) [847ms] | — |
| **乘** | `dʑǐəŋ`→`dZǐ@N` [985ms] | `dʑʰjəŋ`→`dZhj@N` [964ms] | `ʑiɪŋ`→`ZiiN` (×2) [1006ms] | `dźjəng`→`dZj@ng` [899ms] | `dʑʰǐəŋ`→`dZhǐ@N` [1108ms] | `dʑʰi̯əŋ`→`dZhi̯@N` [1108ms] | — |
| **載** | `tsɒi`→`tsQi` (×2) [878ms] | `tsAi`→`tsAi` (×2) [958ms] | `tsəi`→`ts@i` (×2) [929ms] | `tsậi`→`tsai` (×2) [786ms] | `tsəi`→`ts@i` (×2) [929ms] | `tsɑ̆i`→`tsĂi` (×2) [1024ms] | — |
| **彈** | `dɑn`→`dAn` [761ms] | `dʰɑn`→`dhAn` [843ms] | `dɑn`→`dAn` [761ms] | `dân`→`dân` [761ms] | `dʰɑn`→`dhAn` [843ms] | `dʰɑn`→`dhAn` [843ms] | — |
| **便** | `bǐɛn`→`bǐEn` [1014ms] | `bʰjæn`→`bhjan` [910ms] | `biæn`→`bian` [962ms] | `bjiän`→`bjiän` [1085ms] | `bʰǐɛn`→`bhǐEn` [1070ms] | `bʰi̯ɛn`→`bhi̯En` [1070ms] | — |
| **差** | `tʃʰǐe`→`tShǐe` (×4) [1053ms] | `tʃʰje`→`tShje` (×4) [909ms] | `tʂʰiɪ`→`tShii` (×4) [1044ms] | `tṣhjĕ`→`tShjĕ` (×4) [960ms] | `tʃʰǐɛ`→`tShǐE` (×4) [1110ms] | `tʂʰie̯`→`tShie̯` (×2) [1039ms] | `tsʰa`→`tsha` [808ms] |
| **幹** | `kɑn`→`kAn` [793ms] | `kɑn`→`kAn` [793ms] | `kɑn`→`kAn` [793ms] | `kân`→`kân` [793ms] | `kɑn`→`kAn` [793ms] | `kɑn`→`kAn` [793ms] | — |
| **傳** | `ȡǐwɛn`→`tsǐwEn` (×2) [1174ms] | `ȡʰjuæn`→`tshjuan` (×2) [943ms] | `ɖiuæn`→`riuan` (×2) [951ms] | `ḍjwän`→`rjwän` (×2) [990ms] | `ȡʰǐuɛn`→`tshǐuEn` (×2) [1288ms] | `ȡʰi̯wɛn`→`tshi̯wEn` (×2) [1195ms] | — |
| **會** | `ɣuɑi`→`xuAi` (×2) [947ms] | `ɣuɑi`→`xuAi` (×2) [947ms] | `ɣuɑi`→`xuAi` (×2) [947ms] | `ɣwâi`→`xwâi` (×2) [841ms] | `ɣuai`→`xuai` (×2) [861ms] | `ɣwɑi`→`xwAi` (×2) [1011ms] | — |
| **相** | `sǐaŋ`→`sǐaN` [1082ms] | `sjɑŋ`→`sjAN` [910ms] | `siɑŋ`→`siAN` [845ms] | `sjang`→`sjang` [967ms] | `sǐɑŋ`→`sǐAN` [1082ms] | `si̯aŋ`→`si̯aN` [1082ms] | `sjaŋ`→`sjaN` [910ms] |
| **參** | `ʃǐěm`→`Sǐěm` (×4) [1129ms] | `ʃjem`→`Sjem` (×4) [863ms] | `ʂiɪm`→`Siim` (×5) [1011ms] | `ṣjəm`→`Sj@m` (×4) [877ms] | `ʃǐəm`→`Sǐ@m` (×4) [1048ms] | `tʂʰi̯əm`→`tShi̯@m` (×2) [1138ms] | — |
| **惡** | `u`→`u` (×2) [658ms] | `ʔuo`→`?uo` (×2) [725ms] | `ʔuo`→`?uo` (×2) [725ms] | `uo`→`uo` (×2) [673ms] | `ʔu`→`?u` (×2) [711ms] | `ʔuo`→`?uo` (×2) [725ms] | — |
| **泊** | `bɑk`→`bAk` [753ms] | `bʰɑk`→`bhAk` [805ms] | `bɑk`→`bAk` [753ms] | `bâk`→`bâk` [753ms] | `bʰɑk`→`bhAk` [805ms] | `bʰɑk`→`bhAk` [805ms] | — |
| **東** | `tuŋ`→`tuN` [797ms] | `tuŋ`→`tuN` [797ms] | `tuŋ`→`tuN` [797ms] | `tung`→`tung` [867ms] | `toŋ`→`toN` [797ms] | `tuŋ`→`tuN` [797ms] | — |
| **山** | `ʃæn`→`San` [854ms] | `ʃæn`→`San` [854ms] | `ʂæn`→`San` [854ms] | `ṣăn`→`Săn` [690ms] | `ʃɐn`→`San` [854ms] | `ʂăn`→`Săn` [943ms] | `ʃen`→`Sen` [810ms] |
| **水** | `ɕwi`→`Swi` [849ms] | `ɕjuei`→`Sjuei` [833ms] | `ɕiuɪi`→`Siuii` [1282ms] | `śjwi`→`Sjwi` [922ms] | `sǐue`→`sǐue` [1097ms] | `ɕwi`→`Swi` [849ms] | `ɕʷiʔ`→`Swi?` [886ms] |
| **之** | `tɕǐə`→`tSǐ@` [970ms] | `tɕi`→`tSi` [761ms] | `tɕi`→`tSi` [761ms] | `tśï`→`tSï` [660ms] | `tɕǐə`→`tSǐ@` [970ms] | `tɕi`→`tSi` [761ms] | `tɕɨ`→`tS1` [582ms] |
| **日** | `ɽǐět`→`rǐět` [1005ms] | `ȵjet`→`Jjet` [765ms] | `ȵiɪt`→`Jiit` [928ms] | `ńźjĕt`→`ńźjĕt` [1144ms] | `nʑǐet`→`nZǐet` [1072ms] | `ȵʑi̯ĕt`→`JZi̯ĕt` [1070ms] | `ȵit`→`Jit` [756ms] |
| **月** | `ŋǐwɐt`→`Nǐwat` [1080ms] | `ŋjuɐt`→`Njuat` [776ms] | `ŋiuɑt`→`NiuAt` [949ms] | `ngjwɐt`→`ngjwat` [995ms] | `ŋǐuɐt`→`Nǐuat` [1015ms] | `ŋi̯wɐt`→`Ni̯wat` [1080ms] | `ŋʷat`→`Nwat` [760ms] |
| **人** | `ɽǐěn`→`rǐěn` [1065ms] | `ȵjen`→`Jjen` [799ms] | `ȵiɪn`→`Jiin` [962ms] | `ńźjĕn`→`ńźjĕn` [1203ms] | `nʑǐen`→`nZǐen` [1120ms] | `ȵʑi̯ĕn`→`JZi̯ĕn` [1128ms] | `ȵin`→`Jin` [790ms] |
| **大** | `dɑi`→`dAi` (×2) [861ms] | `dʰɑi`→`dhAi` (×2) [943ms] | `dɑi`→`dAi` (×2) [861ms] | `dâi`→`dâi` (×2) [676ms] | `dʰai`→`dhai` (×2) [771ms] | `dʰɑi`→`dhAi` [943ms] | `da`→`da` [689ms] |
| **天** | `tʰien`→`thien` [944ms] | `tʰiɛn`→`thiEn` [816ms] | `tʰiɛn`→`thiEn` [816ms] | `thien`→`thien` [944ms] | `tʰien`→`thien` [944ms] | `tʰien`→`thien` [944ms] | `tʰen`→`then` [772ms] |
| **地** | `di`→`di` [689ms] | `dʰjei`→`dhjei` [854ms] | `diɪi`→`diii` [1018ms] | `dji`→`dji` [755ms] | `dʰǐe`→`dhǐe` [941ms] | `dʰi`→`dhi` [761ms] | `dis`→`dis` [782ms] |
| **馬** | `ma`→`ma` [725ms] | `ma`→`ma` [725ms] | `ma`→`ma` [725ms] | `ma`→`ma` [725ms] | `ma`→`ma` [725ms] | `ma`→`ma` [725ms] | — |
| **風** | `pǐuŋ`→`pǐuN` [1050ms] | `pjuŋ`→`pjuN` [876ms] | `piuŋ`→`piuN` [997ms] | `pjung`→`pjung` [947ms] | `pfǐoŋ`→`pfǐoN` [1153ms] | `pi̯uŋ`→`pi̯uN` [1050ms] | — |
| **雨** | `ɣǐu`→`xǐu` [1013ms] | `ɣjuo`→`xjuo` [841ms] | `jiuo`→`jiuo` [894ms] | `ju`→`ju` [710ms] | `jǐu`→`jǐu` [947ms] | `ji̯u`→`ji̯u` [947ms] | `ɦʷaʔ`→`hwa?` [810ms] |
| **木** | `muk`→`muk` [771ms] | `muk`→`muk` [771ms] | `muk`→`muk` [771ms] | `muk`→`muk` [771ms] | `mok`→`mok` [771ms] | `muk`→`muk` [771ms] | `muk`→`muk` [771ms] |
| **金** | `kǐěm`→`kǐěm` [1068ms] | `kjem`→`kjem` [816ms] | `kiem`→`kiem` [921ms] | `kjəm`→`kj@m` [830ms] | `kǐəm`→`kǐ@m` [987ms] | `ki̯əm`→`ki̯@m` [987ms] | `krim`→`krim` [812ms] |
| **火** | `huɑ`→`huA` [753ms] | `xuɑ`→`xuA` [775ms] | `xuɑ`→`xuA` [775ms] | `xuâ`→`xuâ` [775ms] | `xuɑ`→`xuA` [775ms] | `xuɑ`→`xuA` [775ms] | `hʷaʔ`→`hwa?` [810ms] |
| **田** | `dien`→`dien` [889ms] | `dʰiɛn`→`dhiEn` [819ms] | `diɛn`→`diEn` [747ms] | `dien`→`dien` [889ms] | `dʰien`→`dhien` [961ms] | `dʰien`→`dhien` [961ms] | `den`→`den` [704ms] |
| **年** | `nien`→`nien` [909ms] | `niɛn`→`niEn` [780ms] | `niɛn`→`niEn` [780ms] | `nien`→`nien` [909ms] | `nien`→`nien` [909ms] | `nien`→`nien` [909ms] | `nen`→`nen` [753ms] |

## 碰撞对（原本不同 → 近似后相同）

- 行: 7 体系均覆盖，无并音
- 重: 7 体系均覆盖，无并音
- 樂: 6 体系均覆盖，无并音
- 長: 6 体系均覆盖，无并音
- 得: 6 体系均覆盖，无并音
- 說: 6 体系均覆盖，无并音
- 為: 6 体系均覆盖，无并音
- 華: 6 体系均覆盖，无并音
- **率**（1 对并音）: wangli_mc×karlgren_mc: ʃwi≠ʂwi → 均变 `Swi`
- 王: 7 体系均覆盖，无并音
- 朝: 7 体系均覆盖，无并音
- 中: 7 体系均覆盖，无并音
- 道: 7 体系均覆盖，无并音
- 難: 6 体系均覆盖，无并音
- 好: 7 体系均覆盖，无并音
- 發: 6 体系均覆盖，无并音
- 覺: 6 体系均覆盖，无并音
- 空: 7 体系均覆盖，无并音
- 曲: 6 体系均覆盖，无并音
- 血: 6 体系均覆盖，无并音
- 稱: 6 体系均覆盖，无并音
- 數: 6 体系均覆盖，无并音
- 落: 6 体系均覆盖，无并音
- 種: 6 体系均覆盖，无并音
- 都: 7 体系均覆盖，无并音
- 還: 6 体系均覆盖，无并音
- 乘: 6 体系均覆盖，无并音
- 載: 6 体系均覆盖，无并音
- 彈: 6 体系均覆盖，无并音
- 便: 6 体系均覆盖，无并音
- 差: 7 体系均覆盖，无并音
- 幹: 6 体系均覆盖，无并音
- 傳: 6 体系均覆盖，无并音
- 會: 6 体系均覆盖，无并音
- 相: 7 体系均覆盖，无并音
- 參: 6 体系均覆盖，无并音
- 惡: 6 体系均覆盖，无并音
- 泊: 6 体系均覆盖，无并音
- 東: 6 体系均覆盖，无并音
- **山**（5 对并音）: wangli_mc×zhoufagao_mc: ʃæn≠ʂæn → 均变 `San`; wangli_mc×chenxinxiong_mc: ʃæn≠ʃɐn → 均变 `San`; dongtonghe_mc×zhoufagao_mc: ʃæn≠ʂæn → 均变 `San`; dongtonghe_mc×chenxinxiong_mc: ʃæn≠ʃɐn → 均变 `San`; zhoufagao_mc×chenxinxiong_mc: ʂæn≠ʃɐn → 均变 `San`
- 水: 7 体系均覆盖，无并音
- 之: 7 体系均覆盖，无并音
- 日: 7 体系均覆盖，无并音
- 月: 7 体系均覆盖，无并音
- 人: 7 体系均覆盖，无并音
- 大: 7 体系均覆盖，无并音
- **天**（3 对并音）: wangli_mc×lifanggui_mc: tʰien≠thien → 均变 `thien`; lifanggui_mc×chenxinxiong_mc: thien≠tʰien → 均变 `thien`; lifanggui_mc×karlgren_mc: thien≠tʰien → 均变 `thien`
- 地: 7 体系均覆盖，无并音
- 馬: 6 体系均覆盖，无并音
- 風: 6 体系均覆盖，无并音
- 雨: 7 体系均覆盖，无并音
- 木: 7 体系均覆盖，无并音
- 金: 7 体系均覆盖，无并音
- 火: 7 体系均覆盖，无并音
- 田: 7 体系均覆盖，无并音
- 年: 7 体系均覆盖，无并音

## 汇总

- 覆盖 55 字；产生并音对的字: 3；音频样本: 362（OK）
- 并音 = 该字在某两体系下原始 IPA 不同、但近似后字符串相同（听感上趋同，实际听感差异仍需以 wav 试听为准）
- 时长列是同一构建的 eSpeak 输出，可横向比较“哪个体系读得更长/更短”，但跨 OS/引擎版本不可比（见 baseline manifest）
