import re
import unicodedata
from typing import List

_RE_URL = re.compile(r"\bhttps?://[^\s]+\b", re.IGNORECASE)
_RE_EMAIL = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", re.IGNORECASE)
_RE_TOKEN = re.compile(
    r"https?://[^\s]+|[\wÀ-ÿ]+(?:['’][\wÀ-ÿ]+)?|[^\s\w]",
    re.UNICODE,
)


def normalize_text(text: str) -> str:
    text = text.strip()
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text


def strip_accents(text: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKD", text)
        if unicodedata.category(ch) != "Mn"
    )


def split_sentences_simple(text: str) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []
    parts = re.split(r"(?<=[\.\!\?])\s+", text)
    return [p.strip() for p in parts if p and p.strip()]


def tokenize(text: str) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []
    return _RE_TOKEN.findall(text)


def is_url(token: str) -> bool:
    return bool(_RE_URL.fullmatch(token))


def is_email(token: str) -> bool:
    return bool(_RE_EMAIL.fullmatch(token))
