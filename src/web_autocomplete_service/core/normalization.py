import unicodedata
import re

def normalize(word: str) -> str:
    """normalize given `word`
    
    Removes edge & redundant whitespaces, lower case, interpret unicodes
    """
    normalized = unicodedata.normalize("NFKC", word).strip().casefold()
    normalized = re.compile(r"\s+").sub(" ", normalized)
    return normalized
