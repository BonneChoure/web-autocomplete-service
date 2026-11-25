from fastapi import APIRouter, Depends, Query
from typing import Annotated

from web_autocomplete_service.core.trie import Trie
from web_autocomplete_service.dependencies import get_trie
from web_autocomplete_service.schemas import AutocompleteResponse
from web_autocomplete_service.services.autocomplete import get_autocomplete_terms


router = APIRouter(tags=["autocomplete"])

@router.get("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete(
    trie: Annotated[Trie, Depends(get_trie)],
    query: str = Query(..., min_length=1, max_length=100)
    ):
    return await get_autocomplete_terms(trie, query, settings)