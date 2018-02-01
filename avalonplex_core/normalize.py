import unicodedata
from typing import Dict

from avalonplex_core.utils import invert_dict


def replace_words(source: str, replacement: Dict[str, str]) -> str:
    result = source
    for word in replacement.keys():
        result = result.replace(word, replacement[word])
    return result


def normalize(source: str) -> str:
    content = replace_words(source, _before)
    content = unicodedata.normalize("NFKC", content)
    content = replace_words(content, _after).strip()
    content_source = content
    content = content.replace("  ", " ")
    while content != content_source:
        content_source = content
        content = content.replace("  ", " ")
    return content


_before = {
    "～": "$wave%",
    "＆": "&amp;",
    "\n\n": "$doubleLineBreak%",
    "＜": "〈",
    "＞": "〉"
}

_after = {
    "\n": "",
    "\t": " ",
    **invert_dict(_before),
    "...": "…",
    "．．．": "…",
    "・・・": "…",
    "、、、": "…",
    "! ": "!",
    "。 ": "。",
    "? ": "?"
}


__all__ = [normalize]