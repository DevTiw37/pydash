from models.search import SearchKind, SearchResult
from search.ranker import RankedResult, RankingPolicy, SearchRanker

def make_result(
    name: str = "dump",
    qualified_name: str = "json.dump",
    description: str | None = None,
) -> SearchResult:
    return SearchResult(
        name=name,
        qualified_name=qualified_name,
        kind=SearchKind.FUNCTION,
        module="json",
        endpoint="/function/json/dump",
        description=description,
    )

def test_exact_name_score():
    ranker = SearchRanker()
    result = make_result()

    assert ranker.get_search_score(result, "dump") == 100

def test_exact_qualified_name_score():
    ranker = SearchRanker()
    result = make_result()

    assert ranker.get_search_score(result, "json.dump") == 95

def test_name_prefix_score():
    ranker = SearchRanker()
    result = make_result(name="dumps")

    assert ranker.get_search_score(result, "dump") == 80

def test_qualified_name_suffix_score():
    ranker = SearchRanker()
    result = make_result(
        name="dump",
        qualified_name="some.json.dump",
    )

    assert ranker.get_search_score(result, "json.dump") == 70

def test_contains_score():
    ranker = SearchRanker()
    result = make_result(
        name="dumps",
        qualified_name="json.dumps",
    )

    assert ranker.get_search_score(result, "ump") == 50

def test_description_score():
    ranker = SearchRanker()
    result = make_result(
        description="Serialize an object to JSON.",
    )

    assert ranker.get_search_score(result, "serialize") == 30

def test_no_match_score():
    ranker = SearchRanker()
    result = make_result()

    assert ranker.get_search_score(result, "banana") == 0

def test_multi_term_score():
    ranker = SearchRanker()
    result = make_result()

    matched_terms, total_score = ranker.get_multi_term_score(
        result,
        ["json", "dump"],
    )

    assert matched_terms == 2
    assert total_score == 150

def test_sort_results_prioritizes_matched_terms():
    ranker = SearchRanker()

    result_one = make_result(
        name="encoder",
        qualified_name="json.encoder",
    )

    result_two = make_result(
        name="json",
        qualified_name="json.json",
    )

    results = [
        RankedResult(
            matched_terms=1,
            total_score=100,
            result=result_one,
        ),
        RankedResult(
            matched_terms=2,
            total_score=60,
            result=result_two,
        ),
    ]

    sorted_results = ranker.sort_results(results)

    assert sorted_results[0].result == result_two

def test_sort_results_uses_total_score_after_coverage():
    ranker = SearchRanker()

    result_one = make_result(
        name="one",
        qualified_name="json.one",
    )

    result_two = make_result(
        name="two",
        qualified_name="json.two",
    )

    results = [
        RankedResult(
            matched_terms=2,
            total_score=60,
            result=result_one,
        ),
        RankedResult(
            matched_terms=2,
            total_score=100,
            result=result_two,
        ),
    ]

    sorted_results = ranker.sort_results(results)

    assert sorted_results[0].result == result_two

def test_sort_results_uses_qualified_name_as_tie_breaker():
    ranker = SearchRanker()

    result_one = make_result(
        name="one",
        qualified_name="json.zebra",
    )

    result_two = make_result(
        name="two",
        qualified_name="json.alpha",
    )

    results = [
        RankedResult(
            matched_terms=1,
            total_score=50,
            result=result_one,
        ),
        RankedResult(
            matched_terms=1,
            total_score=50,
            result=result_two,
        ),
    ]


    sorted_results = ranker.sort_results(results)

    assert sorted_results[0].result == result_two

def test_rank_returns_only_matching_results_in_rank_order():
    ranker = SearchRanker()

    matching_result = make_result(
        name="dump",
        qualified_name="json.dump",
    )

    partial_result = make_result(
        name="dumps",
        qualified_name="json.dumps",
    )

    unrelated_result = make_result(
        name="load",
        qualified_name="json.load",
    )

    results = ranker.rank(
        [
            unrelated_result,
            partial_result,
            matching_result,
        ],
        ["dump"],
    )

    assert results == [
        matching_result,
        partial_result,
    ]

def test_custom_ranking_policy_changes_score():
    policy = RankingPolicy(
        exact_name=200,
    )

    ranker = SearchRanker(policy)
    result = make_result()

    assert ranker.get_search_score(result, "dump") == 200
