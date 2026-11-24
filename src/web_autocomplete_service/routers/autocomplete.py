from fastapi import APIRouter

from web_autocomplete_service.schemas import TermList
from web_autocomplete_service.services.autocomplete import get_autocomplete_terms

router = APIRouter(tags=["autocomplete"])

@router.get("/autocomplete", response_model=TermList)
async def autocomplete(query: str):
    return await get_autocomplete_terms(query)