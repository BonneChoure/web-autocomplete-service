from fastapi import Request

from app.core.trie import Trie

def get_trie(request: Request) -> Trie:
    return request.app.state.trie