from config import (
    PACKAGES_TO_INDEX,
    SEARCH_DEFAULT_LIMIT,
    SEARCH_MAX_LIMIT,
)


def test_search_limits_are_configured():
    assert SEARCH_DEFAULT_LIMIT == 20
    assert SEARCH_MAX_LIMIT == 100


def test_packages_to_index_are_configured():
    assert PACKAGES_TO_INDEX == [
        "email",
        "json",
    ]