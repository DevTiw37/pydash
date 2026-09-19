import pytest

from config import PACKAGES_TO_INDEX
from search.index_manager import search_index
from services.search_service import search, search_status


@pytest.fixture(autouse=True)
def initialize_search_index():
    search_index.rebuild(PACKAGES_TO_INDEX)
    yield
    search_index.clear()


def test_search_service_returns_results():
    results = search("dump")

    assert len(results) > 0
    assert results[0].name == "dump"
    assert results[0].qualified_name == "json.dump"


def test_search_service_returns_status():
    status = search_status()

    assert status.ready is True
    assert "json" in status.indexed_packages
    assert status.total_objects > 0


def test_search_service_uses_configured_default_limit():
    results = search("json")

    assert len(results) == 20
