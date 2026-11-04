"""
language/polyphone.py
简繁字形转换（轻量版：opencc）。

东汉官音表以简体字为键（703 字中 701 字），但输入可能是繁体；字形转换
是纯字形映射：简繁同字同音，查表转换不影响读音结果，显示层始终用
用户输入的原字形。第三方《廣韻》表以繁体为键，简体输入反之需转繁。

opencc 缺失（或导入失败）→ 原样返回，只做精确匹配，绝不抛错。
"""

_OPENCC_CACHE = {}


def _opencc_convert(config):
    """懒加载并缓存 opencc 转换器；opencc 不可用时返回 None。"""
    if config not in _OPENCC_CACHE:
        conv = None
        try:
            from opencc import OpenCC
            conv = OpenCC(config)
        except Exception:
            conv = None
        _OPENCC_CACHE[config] = conv
    return _OPENCC_CACHE[config]


def to_simplified(text):
    """繁体 → 简体。opencc 不可用时原样返回（不抛错）。"""
    conv = _opencc_convert("t2s")
    return conv.convert(str(text)) if conv is not None else str(text)


def to_traditional(text):
    """简体 → 繁体。opencc 不可用时原样返回（不抛错）。"""
    conv = _opencc_convert("s2t")
    return conv.convert(str(text)) if conv is not None else str(text)
