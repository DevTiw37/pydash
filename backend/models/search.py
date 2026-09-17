from pydantic import BaseModel

class SearchResult(BaseModel):
    name: str
    qualified_name: str
    kind: str
    module: str
    class_name: str | None = None
    endpoint: str
    description: str | None = None
    
class SearchStatus(BaseModel):
    indexed_packages: list[str]
    failed_packages: dict[str, str]
    total_objects: int
    ready: bool

class SearchResponse(BaseModel):
    # name: str
    query: str
    results: list[SearchResult]