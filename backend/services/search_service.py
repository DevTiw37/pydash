from config import SEARCH_DEFAULT_LIMIT
from search.index_manager import search_index
from models.search import SearchStatus


def search(
    query: str,
    limit: int = SEARCH_DEFAULT_LIMIT,
    kind: str | None = None,
):
    return search_index.search(query, limit, kind)

def search_status() -> SearchStatus:
    return SearchStatus(
        indexed_packages=search_index.packages(),
        failed_packages=search_index.failed_packages(),
        total_objects=search_index.count(),
        ready=search_index.is_ready(),
    )
