from models.search import SearchKind
from search.index_manager import SearchIndex


def test_new_index_is_empty():
    index = SearchIndex()

    assert index.count() == 0
    assert index.packages() == []
    assert index.is_ready() is False
    assert index.failed_packages() == {}

def test_add_package_indexes_objects():
    index = SearchIndex()

    index.add_package("json")

    assert index.count() == 27
    assert index.packages() == ["json"]

def test_add_package_does_not_duplicate_package():
    index = SearchIndex()

    index.add_package("json")
    first_count = index.count()

    index.add_package("json")

    assert index.count() == first_count
    assert index.packages() == ["json"]

def test_filter_results_by_kind():
    index = SearchIndex()

    index.add_package("json")

    functions = index.filter_results(SearchKind.FUNCTION)
    classes = index.filter_results(SearchKind.CLASS)

    assert len(functions) == 12
    assert len(classes) == 3

    assert all(item.kind == SearchKind.FUNCTION for item in functions)
    assert all(item.kind == SearchKind.CLASS for item in classes)

def test_search_returns_ranked_results():
    index = SearchIndex()

    index.add_package("json")

    results = index.search("dump")

    assert len(results) == 2
    assert results[0].qualified_name == "json.dump"
    assert results[1].qualified_name == "json.dumps"

def test_search_filters_by_kind():
    index = SearchIndex()

    index.add_package("json")

    functions = index.search(
        "dump",
        kind=SearchKind.FUNCTION,
    )

    classes = index.search(
        "dump",
        kind=SearchKind.CLASS,
    )

    assert len(functions) == 2
    assert classes == []

    assert all(
        item.kind == SearchKind.FUNCTION
        for item in functions
    )

def test_search_applies_limit():
    index = SearchIndex()

    index.add_package("json")

    results = index.search(
        "json",
        limit=5,
    )

    assert len(results) == 5

def test_rebuild_replaces_existing_index():
    index = SearchIndex()

    index.add_package("json")
    assert index.packages() == ["json"]

    index.rebuild(["email"])

    assert index.packages() == ["email"]
    assert index.count() > 0
    assert index.failed_packages() == {}
    assert index.is_ready() is True

def test_rebuild_records_failed_package_and_continues():
    index = SearchIndex()

    index.rebuild([
        "json",
        "package_that_does_not_exist",
    ])

    assert index.packages() == ["json"]
    assert index.count() > 0
    assert index.is_ready() is True

    failures = index.failed_packages()

    assert "package_that_does_not_exist" in failures
    assert "No module named" in failures["package_that_does_not_exist"]

def test_search_normalizes_multiple_spaces():
    index = SearchIndex()

    index.add_package("json")

    results = index.search("json   dump")

    assert len(results) > 0
    assert results[0].qualified_name == "json.dump"


def test_search_normalizes_dot_separated_query():
    index = SearchIndex()

    index.add_package("json")

    results = index.search("JSON.DUMP")

    assert len(results) > 0
    assert results[0].qualified_name == "json.dump"


def test_search_ignores_punctuation_only_query():
    index = SearchIndex()

    index.add_package("json")

    assert index.search(".") == []
    assert index.search("...") == []