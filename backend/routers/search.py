from fastapi import APIRouter, Query

from models.search import SearchKind, SearchResponse, SearchStatus
from search.index_manager import search_index
from services.search_service import search


router = APIRouter(
    prefix="/search",
    tags=["search"],
)

@router.get("/status", response_model=SearchStatus)
def search_status():
    return SearchStatus(
        indexed_packages=search_index.packages(),
        failed_packages=search_index.failed_packages(),
        total_objects=search_index.count(),
        ready=search_index.is_ready(),
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
