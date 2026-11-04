# -*- coding: utf-8 -*-
"""v4.1.0 回归测试：11/04 QA 修复（v4 行，不含 v5 新功能）。

① [严重] 简繁同字同音：东汉官音表以简体为键，繁体输入（東）应同简体（东）
   读 tuŋ，不落拼音近似层；两种字形都未收录（很）仍如实拼音近似，不伪造。
② 逐字表：analyze_reply 收录行带「韵」字段（如「东韵」），显示保留用户原字形。
④ 大模型回退提示：llm_client 调用失败/未配密钥时 result 带 llm_note，
   选词典或云端成功时不带。

运行：python -m unittest discover -s tests
（opencc 缺失时 ① 的转换断言自动降级：精确命中仍过，转换断言跳过。）
"""
import os
import sys
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from phonology_db import EASTERN_HAN_DB, lookup_char_invariant  # noqa: E402
from language import ancient_tts  # noqa: E402
from language.polyphone import (  # noqa: E402
    to_simplified, to_traditional, _opencc_convert,
)
from services import llm_client  # noqa: E402

_OPENCC_PRESENT = _opencc_convert("t2s") is not None


class TestScriptInvariantLookup(unittest.TestCase):
    """① 字形无关查表（phonology_db.lookup_char_invariant）。"""

    def test_simplified_key_direct_hit(self):
        m, d = lookup_char_invariant("东")
        self.assertEqual(m, "东")
        self.assertEqual(d["ipa"], "tuŋ")
        self.assertEqual(d["final"], "东韵")

    def test_traditional_key_direct_hit(self):
        if "麴" in EASTERN_HAN_DB:
            m, d = lookup_char_invariant("麴")
            self.assertEqual(m, "麴")
            self.assertEqual(d["ipa"], "kʰuk")
        else:
            self.skipTest("麴 不在当前字表")

    def test_missing_in_both_scripts_stays_missing(self):
        self.assertEqual(lookup_char_invariant("很"), (None, None))
        self.assertEqual(lookup_char_invariant("龘"), (None, None))

    @unittest.skipUnless(_OPENCC_PRESENT, "opencc 不在测试环境（转换不可用）")
    def test_converters(self):
        self.assertEqual(to_simplified("東龍書"), "东龙书")
        self.assertEqual(to_traditional("东"), "東")

    @unittest.skipUnless(_OPENCC_PRESENT, "opencc 不在测试环境（转换不可用）")
    def test_traditional_input_hits_simplified_entry(self):
        m, d = lookup_char_invariant("東")
        self.assertEqual(m, "东")
        self.assertEqual(d["ipa"], "tuŋ")
        self.assertEqual(d["final"], "东韵")
        m, d = lookup_char_invariant("龍")
        self.assertEqual(d["ipa"], "ljoŋ")


class TestAncientTtsCoverage(unittest.TestCase):
    """① 合成口径：繁体输入全命中（不降级近似），缺字如实近似。"""

    def test_missing_char_honest_approx_not_fabricated(self):
        # 很：简繁同形且都未收录 → 拼音近似，不伪造 DB 条目
        r = ancient_tts.text_to_ipa("很")
        self.assertEqual(r.coverage, 0)
        self.assertEqual(r.approx, 1)
        self.assertEqual(r.unknown, [])

    @unittest.skipUnless(_OPENCC_PRESENT, "opencc 不在测试环境（转换不可用）")
    def test_traditional_sentence_covered(self):
        # 東/龍 经 t2s 命中简体键 东/龙：coverage=2，无近似
        r = ancient_tts.text_to_ipa("東龍")
        self.assertEqual(r.coverage, 2)
        self.assertEqual(r.approx, 0)
        self.assertEqual(r.unknown, [])
        self.assertIn("tuŋ", r.ipa_text)
        self.assertIn("ljoŋ", r.ipa_text)

    def test_no_opencc_degrades_to_exact_match(self):
        # opencc 不可用：精确命中不受影响；繁体输入退回未命中（不崩溃）
        import language.polyphone as poly
        saved = dict(poly._OPENCC_CACHE)
        poly._OPENCC_CACHE.clear()
        poly._OPENCC_CACHE.update({"t2s": None, "s2t": None})
        try:
            m, d = lookup_char_invariant("东")
            self.assertEqual((m, d["ipa"]), ("东", "tuŋ"))
            if _OPENCC_PRESENT:
                self.assertEqual(lookup_char_invariant("東"), (None, None))
        finally:
            poly._OPENCC_CACHE.clear()
            poly._OPENCC_CACHE.update(saved)


class TestRobotAnalyzeReply(unittest.TestCase):
    """② 逐字表：收录行带韵部字段，显示保留用户原字形。"""

    @classmethod
    def setUpClass(cls):
        try:
            from robot.app import analyze_reply
        except Exception as e:  # 依赖缺失时跳过整类
            raise unittest.SkipTest(f"robot.app 不可导入：{e}")
        cls.analyze_reply = staticmethod(analyze_reply)

    def test_traditional_char_row_keeps_original_form_with_final(self):
        rows = self.analyze_reply("東")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["char"], "東")
        if _OPENCC_PRESENT:
            self.assertEqual(rows[0]["ipa"], "tuŋ")
            self.assertEqual(rows[0]["final"], "东韵")
            self.assertEqual(rows[0]["src"], "收录")
        else:
            self.assertEqual(rows[0]["src"], "拼音近似")

    def test_simplified_char_row_has_final(self):
        rows = self.analyze_reply("东")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["char"], "东")
        self.assertEqual(rows[0]["ipa"], "tuŋ")
        self.assertEqual(rows[0]["final"], "东韵")
        self.assertEqual(rows[0]["src"], "收录")

    def test_missing_char_row_is_pinyin_approx(self):
        rows = self.analyze_reply("很")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["src"], "拼音近似")
        self.assertEqual(rows[0].get("final", ""), "")


class TestLlmFallbackNote(unittest.TestCase):
    """④ 大模型回退提示（services.llm_client.generate_turn）。"""

    def test_no_key_fallback_has_note(self):
        saved = llm_client.API_KEY
        llm_client.API_KEY = ""
        try:
            out = llm_client.generate_turn("你好", mode="api")
        finally:
            llm_client.API_KEY = saved
        self.assertIn("llm_note", out)
        self.assertIn("未配置 LLM_API_KEY", out["llm_note"])

    def test_api_error_fallback_has_note(self):
        import httpx
        saved_call = llm_client._call_chat
        saved_key = llm_client.API_KEY

        def _boom(*a, **k):
            req = httpx.Request("POST", "http://127.0.0.1:0/chat/completions")
            raise httpx.HTTPStatusError(
                "401 Unauthorized",
                request=req, response=httpx.Response(401, request=req))

        llm_client._call_chat = _boom
        llm_client.API_KEY = "dummy-key"
        try:
            out = llm_client.generate_turn("你好", mode="api")
        finally:
            llm_client._call_chat = saved_call
            llm_client.API_KEY = saved_key
        self.assertIn("llm_note", out)
        self.assertIn("401", out["llm_note"])

    def test_dictionary_selection_no_note(self):
        out = llm_client.generate_turn("你好", mode="dictionary")
        self.assertNotIn("llm_note", out)

    def test_cloud_success_no_note(self):
        saved_call = llm_client._call_chat
        saved_key = llm_client.API_KEY
        llm_client._call_chat = lambda *a, **k: {
            "translation": "汝好", "reply": "安", "reply_modern": "你好"}
        llm_client.API_KEY = "dummy-key"
        try:
            out = llm_client.generate_turn("你好", mode="api")
        finally:
            llm_client._call_chat = saved_call
            llm_client.API_KEY = saved_key
        self.assertNotIn("llm_note", out)
        self.assertEqual(out.get("source"), "cloud")


if __name__ == "__main__":
    unittest.main()
