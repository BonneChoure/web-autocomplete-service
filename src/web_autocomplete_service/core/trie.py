from dataclasses import dataclass, field

@dataclass(slots=True)
class TrieNode:
    children: dict[TrieNode] = field(default_factory=dict)
    is_leaf: bool = False
    sorted: bool = True


class Trie: 
    def __init__(self):
        self.root = TrieNode()
        self._unsorted_nodes: list[TrieNode] = []

    def insert(self, word: str) -> None:
        """Insert a word into the Trie"""
        node = self.root
        for letter in word:
            child = node.children.get(letter)
            if child is None:
                if node.sorted and node.children and letter < next(reversed(node.children)):
                    node.sorted = False
                    self._unsorted_nodes.append(node)
                child = TrieNode()
                node.children[letter] = child
            node = child
        node.is_leaf = True
    
    def search(self, prefix: str, limit: int) -> list[str]:
        """Search the closest terms to the given prefix"""
        # Sort the Trie if needed
        if self._unsorted_nodes:
            self._sort()
        
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

    def _retrieve(self, node: TrieNode, path: str, limit: int, suggestions: list[str]) -> None:
        """
        Function used recursively to find first terms starting from a node
        """
        if len(suggestions) > limit:
            return
        
        if node.is_leaf:
            suggestions.append(path)
        
        for childCharacter in (node.children):
            if len(suggestions) >= limit:
                return
            self._retrieve(node.children[childCharacter], path + childCharacter, limit, suggestions)

    def _sort(self):
        for node in self._unsorted_nodes:
            node.children = dict(sorted(node.children.items()))
            node.sorted = True
        self._unsorted_nodes.clear()