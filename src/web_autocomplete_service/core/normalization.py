import unicodedata
import re

def normalize(word: str) -> str:
    normalized = unicodedata.normalize("NFKC", word).strip().casefold()
    normalized = re.compile(r"\s+").sub(" ", normalized)
    return normalized
