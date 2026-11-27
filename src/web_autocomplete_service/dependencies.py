from fastapi import Request

from web_autocomplete_service.core.trie import RadixTrie

def get_trie(request: Request) -> RadixTrie:
    """Return global RadixTrie that stores all words"""
    return request.app.state.trie