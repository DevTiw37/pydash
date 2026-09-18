from fastapi import APIRouter, Query

from models.search import SearchKind, SearchResponse
from services.search_service import search


router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("", response_model=SearchResponse)
def search_endpoint(
    q: str = Query(min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    kind: SearchKind | None = None,
):
    results = search(q, limit, kind)

    return SearchResponse(
        query=q,
        results=results,
    )
