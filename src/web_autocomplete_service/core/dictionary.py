from functools import Path

from web_autocomplete_service.core.trie import Trie
from web_autocomplete_service.core.normalization import normalize

def load_trie(trie: Trie, input_path:Path) -> None:
    with open(input_path, encoding="utf-8") as input_file:
        for line in input_file:
            if line.strip().isalpha(): 
                word = normalize(line)
                trie.insert(word)
            else:
                continue