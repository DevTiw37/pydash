from models.search import SearchResult
from search.index_builder import build_index

class SearchIndex:
    def __init__(self):
        self._index: list[SearchResult] = []
        self._packages: set[str] = set()
        self._failed_packages: dict[str, str] = {}
        self._qualified_names: set[str] = set()
        self._ready = False
        
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
    
    def normalize_query(self, query: str) -> str:
        query = query.strip().lower()
        query = query.replace(" ", ".")

        return query

    def split_query_terms(self, query: str) -> list[str]:
        query = query.strip().lower()

        return query.replace(".", " ").split()

    def get_search_score(
        self,
        item: SearchResult,
        query: str,
    ) -> int:
        query = query.lower()

        name = item.name.lower()
        qualified_name = item.qualified_name.lower()
        description = (item.description or "").lower()

        if name == query:
            return 100

        if name.startswith(query):
            return 80
        
        if qualified_name == query:
            return 95

        if qualified_name.endswith(query):
            return 70

        if query in name or query in qualified_name:
            return 50

        if query in description:
            return 30

        return 0


    def search(
        self,
        query: str,
        limit: int = 20,
        kind: str | None = None,
    ) -> list[SearchResult]:
        query = self.normalize_query(query)
        terms = self.split_query_terms(query)

        if not query:
            return []

        scored_results = []

        for item in self._index:
            if kind is not None and item.kind != kind:
                continue

            if len(terms) == 1:
                score = self.get_search_score(item, terms[0])

                if score > 0:
                    scored_results.append((1, score, item))

            else:
                matched_terms, total_score = self.get_multi_term_score(
                    item,
                    terms,
                )

                if matched_terms > 0:
                    scored_results.append(
                        (matched_terms, total_score, item)
                    )

        scored_results.sort(
            key=lambda result: (
                -result[0],
                -result[1],
                result[2].qualified_name,
            ),
        )

        return [item for _, _, item in scored_results[:limit]]
        
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

    def get_multi_term_score(
        self,
        item: SearchResult,
        terms: list[str],
    ) -> tuple[int, int]:
        matched_terms = 0
        total_score = 0

        for term in terms:
            score = self.get_search_score(item, term)

            if score > 0:
                matched_terms += 1
                total_score += score

        return matched_terms, total_score


search_index = SearchIndex()
