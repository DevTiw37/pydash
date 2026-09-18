from search.ranker import SearchRanker
from models.search import SearchResult
from search.index_builder import build_index
from search.query import SearchQuery

class SearchIndex:
    def __init__(self):
        self._ranker = SearchRanker()
        self._index: list[SearchResult] = []
        self._packages: set[str] = set()
        self._failed_packages: dict[str, str] = {}
        self._qualified_names: set[str] = set()
        self._ready = False
        self._query_parser = SearchQuery()
        
    def clear(self):
        self._index.clear()
        self._packages.clear()
        self._failed_packages.clear()
        self._qualified_names.clear()
        self._ready = False
        
    def add_package(self, package_name: str):
        if package_name in self._packages:
            return

        package_index = build_index(package_name)

        for item in package_index:
            if item.qualified_name in self._qualified_names:
                continue

            self._index.append(item)
            self._qualified_names.add(item.qualified_name)

        self._packages.add(package_name)
        
    def mark_ready(self):
        self._ready = True
        
    def is_ready(self) -> bool:
        return self._ready
    
    def count(self) -> int:
        return len(self._index)
    
    def packages(self) -> list[str]:
        return sorted(self._packages)

    def filter_results(
        self,
        kind: str | None = None,
    ) -> list[SearchResult]:
        if kind is None:
            return self._index

        return [
            item
            for item in self._index
            if item.kind == kind
        ]

    def search(
        self,
        query: str,
        limit: int = 20,
        kind: str | None = None,
    ) -> list[SearchResult]:
        query = self._query_parser.normalize(query)
        terms = self._query_parser.split_terms(query)

        if not query:
            return []

        candidates = self.filter_results(kind)

        ranked_results = self._ranker.rank(
            candidates,
            terms,
        )

        return ranked_results[:limit]
        
    def rebuild(self, package_names: list[str]):
        self.clear()

        for package_name in package_names:
            try:
                self.add_package(package_name)
            except Exception as error:
                self._failed_packages[package_name] = str(error)

        self.mark_ready()
        
    def failed_packages(self) -> dict[str, str]:
        return dict(self._failed_packages)


search_index = SearchIndex()
