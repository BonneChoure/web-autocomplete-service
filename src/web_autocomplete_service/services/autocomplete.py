from web_autocomplete_service.config import get_settings
from web_autocomplete_service.core.trie import Trie
from web_autocomplete_service.core.normalization import normalize

settings = get_settings()

def get_autocomplete_terms(trie: Trie, prefix:str, limit: int = settings.autocomplete_terms_limit) -> list[str]:
    normalized_prefix = normalize(prefix)
    if normalized_prefix is None or not normalized_prefix:
        return []
    return trie.search(normalized_prefix, limit)