from fastapi import Request

from web_autocomplete_service.core.trie import Trie

def get_trie(request: Request) -> Trie:
    return request.app.state.trie