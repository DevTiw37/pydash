from fastapi import APIRouter, Query
from config import SEARCH_DEFAULT_LIMIT, SEARCH_MAX_LIMIT
from models.search import SearchKind, SearchResponse, SearchStatus
from services.search_service import search, search_status


router = APIRouter(
    prefix="/search",
    tags=["search"],
)

@router.get("/status", response_model=SearchStatus)
def search_status_endpoint():
    return search_status()

@router.get("", response_model=SearchResponse)
def search_endpoint(
    q: str = Query(min_length=1),
    limit: int = Query(
        default=SEARCH_DEFAULT_LIMIT,
        ge=1,
        le=SEARCH_MAX_LIMIT,
    ),
    kind: SearchKind | None = None,
):
    results = search(q, limit, kind)

    return SearchResponse(
        query=q,
        results=results,
    )
