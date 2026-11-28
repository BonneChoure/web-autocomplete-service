from dataclasses import dataclass, field

"""This module allow to store a dictionary into a Radix Trie (or Radix tree).

A traditional Trie structure stores each character as a node

    Example:
    Words: duck, ducky, duckling.

    root
    └── d
        └── u
            └── c
                └── k *
                    ├──l
                    |  └──i
                    |     └──n
                    |        └──g *
                    └── y *
    * marks the end of a word

A Radix Trie merge consecutive nodes with a single child that do not end a word.

    Example with a Radix trie:
    root
    └──duck*
        └──ling*
        └──y*
    * marks the end of a word
"""

@dataclass(slots=True)
class RadixNode:
    label: str = ""
    children: dict[str, "RadixNode"] = field(default_factory=dict)
    is_end_of_word: bool = False
    is_sorted: bool = True

class RadixTrie: 
    """Store words in a Radix Trie for prefix search.
    
    Node's children are keyed with the first character of the child's label.
    The unsorted nodes are sorted when the search function is called.
    """

    def __init__(self):
        self.root = RadixNode()
        self._unsorted_nodes: list[RadixNode] = []

    def _add_child(self, parent_node: RadixNode, child_node: RadixNode):
        key = child_node.label[0]
        if parent_node.is_sorted and parent_node.children and key < next(reversed(parent_node.children)):
            parent_node.is_sorted = False
            self._unsorted_nodes.append(parent_node)
        parent_node.children[key] = child_node

    def insert(self, word: str) -> None:
        """Insert a word into the RadixTrie
        
        Add nodes to the unsorted nodes list when needed.
        """
        
        node = self.root
        rest = word

        while True:
            if not rest:
                # Word stops at a node
                node.is_end_of_word = True
                return
            
            child = node.children.get(rest[0])
            if child is None:
                self._add_child(node, RadixNode(is_end_of_word = True, label=rest))
                return

            # Child starting with same letter as rest exists
            i = 0
            max_common_length = min(len(child.label), len(rest))

            # Identifying where the rest and the child label diverge
            while i < max_common_length and child.label[i] == rest[i]:
                i += 1

            if i < len(child.label):
                # Common characters stopped in the middle of the child label
                # New mid node creation : "abcdef" -> "abc" + "def"
                mid = RadixNode(label=child.label[:i])
                child.label = child.label[i:]
                mid.children[child.label[0]] = child
                node.children[rest[0]] = mid
                child = mid
            node, rest = child, rest[i:]

    def _retrieve(self, node: RadixNode, path: str, limit: int, suggestions: list[str]) -> None:
        if node.is_end_of_word:
            suggestions.append(path)
        
        for child in node.children.values():
            if len(suggestions) >= limit:
                return
            self._retrieve(child, path + child.label, limit, suggestions)

    def search(self, prefix: str, limit: int) -> list[str]:
        """Search up to `limit` first alphabetically sorted terms to the given `prefix`
        
        Returns an empty array if nothing matches or if `limit` is not strictly positive.
        """
        if limit <= 0:
            return []

        # Sort the Trie if needed
        if self._unsorted_nodes:
            self.sort()

        # Looking for the prefix first
        rest = prefix
        node = self.root
        path = "" # to track where we are in the Trie
        while rest:
            child = node.children.get(rest[0])
            if child is None:
                return []

            max_common_length = min(len(child.label), len(rest))
            if rest[:max_common_length] != child.label[:max_common_length]:
                return []

            path = path + child.label
            node = child
            rest = rest[max_common_length:]

        # Looking for suggestions then
        suggestions = []
        self._retrieve(node, path, limit, suggestions)
        return suggestions

    def sort(self):
        for node in self._unsorted_nodes:
            node.children = dict(sorted(node.children.items()))
            node.is_sorted = True
        self._unsorted_nodes.clear()