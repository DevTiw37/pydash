from search.index_manager import search_index


def search(
    query: str,
    limit: int = 20,
    kind: str | None = None,
):
    return search_index.search(query, limit, kind)