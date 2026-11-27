from fastapi import APIRouter, Depends, Query
from typing import Annotated

from web_autocomplete_service.config import get_settings
from web_autocomplete_service.core.trie import RadixTrie
from web_autocomplete_service.dependencies import get_trie
from web_autocomplete_service.schemas import AutocompleteResponse
from web_autocomplete_service.services.autocomplete import get_autocomplete_terms

router = APIRouter(tags=["autocomplete"])
settings = get_settings()

@router.get("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete(
    trie: Annotated[RadixTrie, Depends(get_trie)],
    query: str = Query(..., min_length=1, 
                       max_length=settings.max_query_length,
                       description="Prefix entered by the user. Case-insensitive."
                )
    ):
    """Return the terms that start with `query`"""
    return get_autocomplete_terms(trie, query)