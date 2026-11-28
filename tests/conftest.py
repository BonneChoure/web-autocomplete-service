import pytest
import os

from pathlib import Path
from fastapi.testclient import TestClient

from web_autocomplete_service.config import get_settings
from web_autocomplete_service.core.trie import RadixTrie
from web_autocomplete_service.main import app

WORDS = ["cryptanalysis", "cryptographers", "cryptographic algorithm", "cryptography", "cryptomancer"]

settings = get_settings()

@pytest.fixture
def trie() -> RadixTrie:
    trie = RadixTrie()
    for w in WORDS:
        trie.insert(w)
    return trie

@pytest.fixture
def dictionary_file(tmp_path):
    p = tmp_path / "dictionary.txt"
    p.write_text("\n".join(WORDS), encoding="utf-8")
    return p


@pytest.fixture
def client(monkeypatch, dictionary_file):
    monkeypatch.setattr(settings, "input_dictionary_path", dictionary_file)
    with TestClient(app) as client:
        yield client