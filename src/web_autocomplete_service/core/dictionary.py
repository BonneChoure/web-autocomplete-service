from pathlib import Path

from web_autocomplete_service.core.trie import RadixTrie
from web_autocomplete_service.core.normalization import normalize

def load_trie(trie: RadixTrie, input_path:Path) -> None:
    with open(input_path, encoding="utf-8") as input_file:
        for line in input_file:
            word = normalize(line)
            trie.insert(word)
    return trie