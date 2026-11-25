from dataclasses import dataclass, field

from web_autocomplete_service.config import get_settings

settings = get_settings()

@dataclass(slots=True)
class TrieNode:
    children: dict[TrieNode] = field(default_factory=dict)
    is_leaf: bool = False


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
    
    def search(self, prefix: str, limit: int = settings.autocomplete_terms_limit) -> list[str]:
        """Search the closest terms to the given prefix"""
        
        # Looking for the prefix first
        node = self.root
        for character in prefix:
            node = node.children.get(character)
            if node is None:
                return []

        # Looking for suggestions then
        suggestions = []
        self._retrieve(node, prefix, limit, suggestions)
        return suggestions

    def _retrieve(self, node: TrieNode, path: str, limit: int, suggestions: list[str]):
        """
        Function used recursively to find first alphabetically sorted terms starting from a node
        """
        if len(suggestions) > limit:
            return
        
        if node.is_leaf:
            suggestions.append(path)
        
        for childCharacter in sorted(node.children):
            if len(suggestions) >= limit:
                return
            self._retrieve(node.children[childCharacter], path + childCharacter, limit, suggestions)

