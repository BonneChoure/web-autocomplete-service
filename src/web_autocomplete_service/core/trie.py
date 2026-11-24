from dataclasses import dataclass, field

from web_autocomplete_service.config import get_settings

settings = get_settings()

@dataclass
class TrieNode(slots=True):
    children: dict[TrieNode] = field(default_factory=dict)
    is_leaf: bool


class Trie: 
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the Trie"""
        node = self.root
        for letter in word:
            child = node.children.get(letter)
            if child is None:
                child = node.children[letter] = TrieNode()
            node = child
        node.is_leaf = True
    
    def search(self, prefix: str, limit: int = settings.autocomplete_terms_limit) -> list[str] | None:
        """Search the closest terms to the given prefix"""
        pass
    
