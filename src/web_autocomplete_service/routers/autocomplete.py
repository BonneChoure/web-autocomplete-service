from fastapi import APIRouter

from web_autocomplete_service.schemas import AutocompleteResponse
from web_autocomplete_service.services.autocomplete import get_autocomplete_terms

router = APIRouter(tags=["autocomplete"])

@router.get("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete(query: str):
    return await get_autocomplete_terms(query)