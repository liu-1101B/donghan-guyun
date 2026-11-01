"""Smoke test: render the robot Streamlit app without microphone or network access."""
import unittest
from pathlib import Path


class RobotAppSmokeTests(unittest.TestCase):
    def test_app_renders_without_hardware_or_vosk_model(self):
        from streamlit.testing.v1 import AppTest

        root = Path(__file__).resolve().parents[1]
        app = root / "robot" / "app.py"
        test_app = AppTest.from_file(str(app), default_timeout=45).run()
        self.assertFalse(
            test_app.exception,
            "Streamlit app raised during initial render: "
            + "; ".join(str(item) for item in test_app.exception),
        )

    def test_ancient_mode_renders_system_selectbox_and_research_panels(self):
        """v5: 东汉古韵模式渲染拟音体系下拉（默认东汉官音）+ 三个研究面板。"""
        from streamlit.testing.v1 import AppTest

        root = Path(__file__).resolve().parents[1]
        app = root / "robot" / "app.py"
        at = AppTest.from_file(str(app), default_timeout=45)
        at.session_state["robot_mode"] = "东汉古韵"
        at.run()
        self.assertFalse(
            at.exception,
            "Streamlit app raised during ancient-mode render: "
            + "; ".join(str(item) for item in at.exception),
        )
        sys_boxes = [b for b in at.selectbox if b.label == "拟音体系"]
        self.assertEqual(len(sys_boxes), 1, "拟音体系下拉未渲染")
        self.assertEqual(sys_boxes[0].value, "东汉洛阳官音（默认）")
        self.assertIn("王力系統·中古（wangli_mc）", sys_boxes[0].options)
        self.assertIn("王力系統·上古（wangli_oc）", sys_boxes[0].options)
        expander_titles = {e.label for e in at.expander}
        for expected in ("🧭 历史音系探索（逐字数据库）",
                         "🔀 同字跨体系对照（争议项）",
                         "🏛️ 中央研究院古今音资料库（来源可追溯的原始记录）"):
            self.assertIn(expected, expander_titles, f"研究面板缺失: {expected}")


class WorkerFourAudioTests(unittest.TestCase):
    """Phase 4 (1): _gen_worker 四段音频 payload（新增中古 reply_mc）。

    LLM / TTS / 声卡全部打桩：只验证调度与 payload 形状，不触网不触硬件。
    """

    def _run_worker(self, generate_turn):
        import robot.app as ra
        from robot.session import Session
        import services.llm_client as llm_client
        import services.tts_client as tts_client

        orig = (llm_client.generate_turn, tts_client.speak_natural,
                ra.get_audio_io)
        try:
            llm_client.generate_turn = generate_turn
            tts_client.speak_natural = lambda *a, **k: b"MP3FAKE"

            def _no_audio_io():
                raise RuntimeError("headless test: no audio device")

            ra.get_audio_io = _no_audio_io
            job = {}
            cfg = {"text": "你好", "mode": "ancient", "mode_label": "古韵",
                   "llm_mode": "dictionary", "voice": "zh-CN-YunxiNeural",
                   "rate": "-10%", "speed": 1.0, "pitch": 130}
            ra._gen_worker(job, Session(), cfg)
            return job
        finally:
            (llm_client.generate_turn, tts_client.speak_natural,
             ra.get_audio_io) = orig

    def test_reply_path_has_four_audio_slots(self):
        def gen(text, history=None, mode="dictionary",
                allow_llm_translate=False):
            return {"translation": "天子", "reply": "善哉",
                    "reply_modern": "好啊", "source": "local-dictionary"}

        job = self._run_worker(gen)
        kind, res = job["result"]
        self.assertEqual(kind, "ok")
        # ② 翻译来源字段进入 payload（桩未提供 → 空串，界面不标注）
        self.assertEqual(res["translation_source"], "")
        self.assertEqual(res["missed_chars"], [])
        audios = res["audios"]
        self.assertEqual(set(audios), {"user", "reply_anc", "reply_mc",
                                       "reply_mod"})
        self.assertTrue(audios["user"]["data"])
        self.assertTrue(audios["reply_anc"]["data"])
        mc = audios["reply_mc"]
        self.assertTrue(mc["data"], "中古音频未产出")
        self.assertEqual(mc["system"], "wangli_mc")
        self.assertEqual(mc["system_label"], "王力系統")
        self.assertTrue(mc["ipa"])
        self.assertEqual(mc["coverage"], 100.0)
        self.assertEqual(audios["reply_mod"]["data"], b"MP3FAKE")
        self.assertTrue(job.get("play_done") is True)

    def test_no_reply_path_keeps_reply_mc_honest_empty(self):
        def gen(text, history=None, mode="dictionary",
                allow_llm_translate=False):
            return {"translation": "量子计算", "reply": "",
                    "reply_modern": "", "source": "local-dictionary-miss",
                    "translation_source": "dictionary",
                    "missed_chars": ["量", "子", "计", "算"]}

        job = self._run_worker(gen)
        kind, res = job["result"]
        self.assertEqual(kind, "ok")
        # ② 未命中的缺字如实透传到 payload
        self.assertEqual(res["translation_source"], "dictionary")
        self.assertEqual(res["missed_chars"], ["量", "子", "计", "算"])
        mc = res["audios"]["reply_mc"]
        self.assertEqual(mc["data"], b"")
        self.assertEqual(mc["ipa"], "")
        self.assertEqual(mc["unknown"], [])
        # v5 新键在默认（无学者体系）路径上保持诚实的缺省值
        self.assertIsNone(res["system_id"])
        self.assertEqual(res["middle_note"], "")
        self.assertEqual(res["scholar_rows"], [])


class WorkerScholarSystemTests(unittest.TestCase):
    """v5: worker 按所选学者拟音体系合成 + 逐字双列数据 + 中古槽自动避让。"""

    def _run_worker(self, generate_turn, system_id, system_label):
        import robot.app as ra
        from robot.session import Session
        import services.llm_client as llm_client
        import services.tts_client as tts_client

        orig = (llm_client.generate_turn, tts_client.speak_natural,
                ra.get_audio_io)
        try:
            llm_client.generate_turn = generate_turn
            tts_client.speak_natural = lambda *a, **k: b"MP3FAKE"

            def _no_audio_io():
                raise RuntimeError("headless test: no audio device")

            ra.get_audio_io = _no_audio_io
            job = {}
            cfg = {"text": "你好", "mode": "ancient", "mode_label": "古韵",
                   "llm_mode": "dictionary", "voice": "zh-CN-YunxiNeural",
                   "rate": "-10%", "speed": 1.0, "pitch": 130,
                   "system_id": system_id, "system_label": system_label}
            ra._gen_worker(job, Session(), cfg)
            return job
        finally:
            (llm_client.generate_turn, tts_client.speak_natural,
             ra.get_audio_io) = orig

    def test_wangli_mc_builds_scholar_rows_and_swaps_mc_slot(self):
        def gen(text, history=None, mode="dictionary",
                allow_llm_translate=False):
            return {"translation": "天子", "reply": "善哉",
                    "reply_modern": "好啊", "source": "local-dictionary"}

        job = self._run_worker(gen, "wangli_mc", "王力系統（中古）")
        kind, res = job["result"]
        self.assertEqual(kind, "ok")
        self.assertEqual(res["system_id"], "wangli_mc")
        self.assertEqual(res["system_label"], "王力系統（中古）")
        # 主体系＝中古槽默认（王力中古）→ 自动避让董同龢中古，避免同体系自对照
        self.assertIn("自动改用", res["middle_note"])
        self.assertEqual(res["audios"]["reply_mc"]["system"], "dongtonghe_mc")
        # reply_anc 按所选体系合成，逐字数据进入 payload
        anc = res["audios"]["reply_anc"]
        self.assertEqual(anc["system"], "wangli_mc")
        self.assertTrue(anc["data"], "所选体系的古韵音频未产出")
        self.assertTrue(anc["ipa"])
        self.assertGreaterEqual(anc["coverage"], 50.0)
        # 逐字双列：键齐整；缺字不补拼音（ipa=None）
        rows = res["scholar_rows"]
        self.assertTrue(rows, "scholar_rows 为空")
        for row in rows:
            self.assertEqual(set(row), {"char", "ipa", "status", "cap"})
            if row["status"] == "缺字（不补拼音）":
                self.assertIsNone(row["ipa"])
        self.assertIsInstance(res["scholar_counts"], dict)
        self.assertTrue(job.get("play_done") is True)


if __name__ == "__main__":
    unittest.main()
