from dataclasses import dataclass, field

@dataclass(slots=True)
class RadixNode:
    label: str = ""
    children: dict[str, "RadixNode"] = field(default_factory=dict)
    is_leaf: bool = False
    is_sorted: bool = True


class RadixTrie: 
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
        """Insert a word into the Trie"""
        
        node = self.root
        rest = word

        while True:
            if not rest:
                node.is_leaf = True
                return
            
            child = node.children.get(rest[0])
            if child is None:
                self._add_child(node, RadixNode(is_leaf = True, label=rest))
                return

            i = 0
            max_common_length = min(len(child.label), len(rest))

            while i < max_common_length and child.label[i] == rest[i]:
                i += 1
            
            if i < len(child.label):
                # New node creation: "abcdef" -> "abc" + "def"
                mid = RadixNode(label=child.label[:i])
                child.label = child.label[i:]
                mid.children[child.label[0]] = child
                node.children[rest[0]] = mid
                child = mid
            node, rest = child, rest[i:]
    
    def search(self, prefix: str, limit: int) -> list[str]:
        """Search the closest terms to the given prefix"""
        if limit <= 0:
            return []

        # Sort the Trie if needed
        if self._unsorted_nodes:
            self._sort()

        # Looking for the prefix first
        rest = prefix
        node = self.root
        path = ""
        suggestions = []  
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

    def _retrieve(self, node: RadixNode, path: str, limit: int, suggestions: list[str]) -> None:
        """
        Function used recursively to find first terms starting from a node
        """
        if node.is_leaf:
            suggestions.append(path)
        
        for child in node.children.values():
            if len(suggestions) >= limit:
                return
            self._retrieve(child, path + child.label, limit, suggestions)

    def _sort(self):
        for node in self._unsorted_nodes:
            node.children = dict(sorted(node.children.items()))
            node.is_sorted = True
        self._unsorted_nodes.clear()