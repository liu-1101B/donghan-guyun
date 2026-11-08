"""Regression tests for explicit missing-data and provenance handling."""
import unittest
from unittest.mock import patch

from language.ancient_tts import text_to_ipa, synthesize_ancient
from language.provenance import get_legacy_entry_provenance, modern_pinyin_approximation_provenance
from phonology_db import lookup_char_record


class LegacyApproximationPolicyTests(unittest.TestCase):
    def test_known_entry_keeps_legacy_ipa_and_is_unassessed(self):
        result = text_to_ipa("东")
        self.assertEqual(result.ipa_text, "tuŋ")
        self.assertEqual(result.coverage, 1)
        self.assertEqual(result.entries[0]["status"], "recorded")
        self.assertEqual(result.entries[0]["provenance"]["confidence"], "unassessed")
        self.assertFalse(get_legacy_entry_provenance("东").is_traceable)

    @patch("language.ancient_tts.get_pinyin_fallback", return_value="hen")
    def test_unlisted_character_missing_by_default(self, _):
        result = text_to_ipa("很")
        self.assertEqual(result.ipa_text, "")
        self.assertEqual(result.unknown, ["很"])
        self.assertEqual(result.entries[0]["status"], "missing")

    @patch("language.ancient_tts.get_pinyin_fallback", return_value="hen")
    def test_modern_pinyin_requires_explicit_opt_in(self, _):
        result = text_to_ipa("很", allow_pinyin_approx=True)
        self.assertTrue(result.ipa_text)
        self.assertEqual(result.approx, 1)
        self.assertEqual(result.entries[0]["status"], "modern_pinyin_approximation")
        self.assertEqual(result.entries[0]["provenance"]["method"], "modern_pinyin_approximation")
        self.assertEqual(modern_pinyin_approximation_provenance().confidence, "unassessed")

    @patch("language.ancient_tts.get_pinyin_fallback", return_value="hen")
    def test_missing_characters_are_in_coverage_denominator(self, _):
        result = text_to_ipa("东很")
        self.assertEqual(result.total, 2)
        self.assertEqual(result.coverage_pct, 50.0)

    def test_invalid_provenance_values_rejected(self):
        from language.provenance import ReadingProvenance
        with self.assertRaises(ValueError):
            ReadingProvenance(system_id="x", system_name="x", scholar="x", method="bad")

    def test_database_record_api_exposes_provenance(self):
        record = lookup_char_record("东")
        self.assertEqual(record["reading"]["ipa"], "tuŋ")
        self.assertEqual(record["provenance"]["confidence"], "unassessed")

    @patch("language.ancient_tts.get_pinyin_fallback", return_value="hen")
    @patch("language.ancient_tts.synthesize_text")
    def test_missing_char_does_not_generate_historical_audio(self, synthesize_mock, _):
        wav, result = synthesize_ancient("很")
        self.assertEqual(wav, b"")
        self.assertEqual(result.unknown, ["很"])
        synthesize_mock.assert_not_called()

    @patch("language.ancient_tts.get_pinyin_fallback", return_value="hen")
    @patch("language.ancient_tts.synthesize_text", return_value=[0.1, 0.2])
    @patch("language.ancient_tts.audio_to_wav_bytes", return_value=b"wav")
    def test_opt_in_approximation_reaches_audio_engine(self, wav_mock, synthesize_mock, _):
        wav, result = synthesize_ancient("很", allow_pinyin_approx=True)
        self.assertEqual(wav, b"wav")
        self.assertEqual(result.approx, 1)
        synthesize_mock.assert_called_once()
        wav_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
