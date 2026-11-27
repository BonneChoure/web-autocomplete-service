from fastapi import Request

from web_autocomplete_service.core.trie import RadixTrie

def get_trie(request: Request) -> RadixTrie:
    return request.app.state.trie