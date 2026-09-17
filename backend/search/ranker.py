from models.search import SearchResult


RankedResult = tuple[int, int, SearchResult]

class SearchRanker:
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

        if qualified_name == query:
            return 95

        if name.startswith(query):
            return 80

        if qualified_name.endswith(query):
            return 70

        if query in name or query in qualified_name:
            return 50

        if query in description:
            return 30

        return 0

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

    def get_result_score(
        self,
        item: SearchResult,
        terms: list[str],
    ) -> tuple[int, int]:
        if len(terms) == 1:
            score = self.get_search_score(item, terms[0])

            if score > 0:
                return 1, score

            return 0, 0

        return self.get_multi_term_score(item, terms)

    def normalize_query(self, query: str) -> str:
        query = query.strip().lower()
        query = query.replace(" ", ".")

        return query

    def split_query_terms(self, query: str) -> list[str]:
        query = query.strip().lower()
        return query.replace(".", " ").split()

    def sort_results(
        self,
        results: list[RankedResult],
    ) -> list[RankedResult]:
        return sorted(
            results,
            key=lambda result: (
                -result[0],
                -result[1],
                result[2].qualified_name,
            ),
        )

    def limit_results(
        self,
        results: list[RankedResult],
        limit: int,
    ) -> list[RankedResult]:
        return results[:limit]
