from web_autocomplete_service.services.autocomplete import get_autocomplete_terms
from web_autocomplete_service.config import get_settings

settings = get_settings()

def test_query_is_normalized(trie):
    assert get_autocomplete_terms(trie, "CRYPT", limit=4) == get_autocomplete_terms(trie, "crypt", limit=4)

def test_results_are_limited(trie):
    assert len(get_autocomplete_terms(trie, "crypt", limit=3)) == 3

def test_default_limit_is_used(trie):
    assert len(get_autocomplete_terms(trie, "crypt")) == settings.autocomplete_terms_limit

def test_whitespace_only_query_returns_empty(trie):
    assert get_autocomplete_terms(trie, "  ") == []

