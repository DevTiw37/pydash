from pydantic import BaseModel


class SearchResult(BaseModel):
    name: str
    qualified_name: str
    kind: str


class SearchResponse(BaseModel):
    # name: str
    query: str
    results: list[SearchResult]