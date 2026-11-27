import pytest

from web_autocomplete_service.core.trie import RadixTrie

def build(words: list[str]):
    trie = RadixTrie()
    for word in words:
        trie.insert(word)
    return trie

# ---- search function ----

def test_results_are_alphabetical():
    trie = build(["exit", "exfiltration", "exhaustive"])
    assert trie.search("ex", limit=4) == ["exfiltration", "exhaustive", "exit"]

def test_results_are_limited(trie):
    assert trie.search("crypt", limit=4) == [
        "cryptanalysis",
        "cryptographers",
        "cryptographic algorithm",
        "cryptography"
    ]

def test_empty_prefix_returns_nothing(trie):
    assert trie.search("bakery", limit=4) == []

def test_partial_prefix_returns_nothing(trie):
    assert trie.search("crypo", limit=4) == []

def test_prefix_that_is_a_complete_word(trie):
    assert trie.search("cryptanalysis", limit=4) == ["cryptanalysis"]

def test_multi_words_terms_keep_intact(trie):
    assert trie.search("cryptographic algo", limit=4) == ["cryptographic algorithm"]

# ---- insert function ----

def test_insert_duplicate_word_does_not_duplicate_results(trie):
    trie.insert("cryptanalysis")
    assert trie.search("crypta", limit=4) == ["cryptanalysis"]

@pytest.mark.parametrize("prefix", ["😄", "有效", "<", "!", "\x00", "\u00a3"])
def test_special_characters_do_not_break(prefix, trie):
    assert trie.search(prefix, limit=4) == []

