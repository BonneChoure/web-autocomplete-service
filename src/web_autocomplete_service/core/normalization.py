import unicodedata

def normalize(word: str) -> str:
    return unicodedata.normalize("NFKC", word).strip().casefold()
