from dataclasses import dataclass

from models.search import SearchResult


@dataclass(frozen=True)
class RankedResult:
    matched_terms: int
    total_score: int
    result: SearchResult


@dataclass(frozen=True)
class RankingPolicy:
    exact_name: int = 100
    exact_qualified_name: int = 95
    name_prefix: int = 80
    qualified_name_suffix: int = 70
    name_contains: int = 50
    description_contains: int = 30


class SearchRanker:
    def __init__(
        self,
        policy: RankingPolicy | None = None,
    ):
        self.policy = policy or RankingPolicy()

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
            return self.policy.exact_name

        if qualified_name == query:
            return self.policy.exact_qualified_name

        if name.startswith(query):
            return self.policy.name_prefix

        if qualified_name.endswith(query):
            return self.policy.qualified_name_suffix

        if query in name or query in qualified_name:
            return self.policy.name_contains

        if query in description:
            return self.policy.description_contains

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

    def sort_results(
        self,
        results: list[RankedResult],
    ) -> list[RankedResult]:
        return sorted(
            results,
            key=lambda result: (
                -result.matched_terms,
                -result.total_score,
                result.result.qualified_name,
            ),
        )

    def rank(
        self,
        items: list[SearchResult],
        terms: list[str],
    ) -> list[SearchResult]:
        scored_results: list[RankedResult] = []

        for item in items:
            matched_terms, total_score = self.get_result_score(
                item,
                terms,
            )

            if matched_terms > 0:
                scored_results.append(
                    RankedResult(
                        matched_terms=matched_terms,
                        total_score=total_score,
                        result=item,
                    )
                )

        scored_results = self.sort_results(scored_results)

        return [
            ranked_result.result
            for ranked_result in scored_results
        ]