"""Evidence metadata for historical reading records."""
from dataclasses import asdict, dataclass
from typing import Optional

CONFIDENCE_LEVELS = frozenset({"high", "medium", "low", "unassessed"})
METHODS = frozenset({
    "direct_transcription", "rule_derived", "scholar_reconstruction",
    "modern_pinyin_approximation", "legacy_unverified",
})


@dataclass(frozen=True, slots=True)
class ReadingProvenance:
    system_id: str
    system_name: str
    scholar: str
    source_id: Optional[str] = None
    source_title: Optional[str] = None
    source_author: Optional[str] = None
    source_url: Optional[str] = None
    source_version: Optional[str] = None
    source_location: Optional[str] = None
    method: str = "legacy_unverified"
    confidence: str = "unassessed"
    note: str = ""

    def __post_init__(self):
        if self.method not in METHODS:
            raise ValueError(f"unsupported provenance method: {self.method}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported confidence level: {self.confidence}")

    @property
    def is_traceable(self) -> bool:
        return bool(self.source_id or self.source_url or self.source_location)

    def to_dict(self) -> dict:
        return asdict(self)


LEGACY_EASTERN_HAN = ReadingProvenance(
    system_id="han_eastern_experimental",
    system_name="东汉洛阳官音（项目实验方案）",
    scholar="项目内部实验方案；具体构拟归属待核",
    method="legacy_unverified",
    confidence="unassessed",
    note="沿用项目早期实验字表；逐字来源、版本及页码尚待核验。",
)
LEGACY_ENTRY_PROVENANCE = {}


def get_legacy_entry_provenance(character: str) -> ReadingProvenance:
    if len(character) != 1:
        raise ValueError("character must contain exactly one code point")
    return LEGACY_ENTRY_PROVENANCE.get(character, LEGACY_EASTERN_HAN)


def modern_pinyin_approximation_provenance() -> ReadingProvenance:
    return ReadingProvenance(
        system_id="modern_mandarin_approximation",
        system_name="现代普通话近似（非历史音系）",
        scholar="现代普通话拼音回退",
        method="modern_pinyin_approximation",
        confidence="unassessed",
        note="由现代拼音转换得到，仅作用户主动开启的占位近似，不代表历史拟音。",
    )
