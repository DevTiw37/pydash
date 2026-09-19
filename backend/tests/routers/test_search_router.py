from fastapi import FastAPI
from fastapi.testclient import TestClient

from models.search import SearchKind, SearchResult, SearchStatus
from routers.search import router


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


def test_search_router_returns_search_results(monkeypatch):
    expected_result = SearchResult(
        name="dump",
        qualified_name="json.dump",
        kind=SearchKind.FUNCTION,
        module="json",
        class_name=None,
        endpoint="/function/json/dump",
        description="Serialize an object to a JSON formatted stream.",
    )

    def fake_search(query, limit=20, kind=None):
        assert query == "dump"
        assert limit == 5
        assert kind == "function"
        return [expected_result]

    monkeypatch.setattr("routers.search.search", fake_search)

    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "limit": 5,
                "kind": "function",
            },
        )

    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "dump"
    assert len(data["results"]) == 1
    assert data["results"][0]["qualified_name"] == "json.dump"


def test_search_status_router_returns_status(monkeypatch):
    expected_status = SearchStatus(
        indexed_packages=["json"],
        failed_packages={},
        total_objects=27,
        ready=True,
    )

    def fake_search_status():
        return expected_status

    monkeypatch.setattr(
        "routers.search.search_status",
        fake_search_status,
    )

    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/search/status")

    assert response.status_code == 200
    assert response.json() == expected_status.model_dump()

def test_search_router_rejects_missing_query():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/search")

    assert response.status_code == 422


def test_search_router_rejects_empty_query():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={"q": ""},
        )

    assert response.status_code == 422


def test_search_router_rejects_invalid_kind():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "kind": "invalid",
            },
        )

    assert response.status_code == 422


def test_search_router_rejects_invalid_limit():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "limit": 0,
            },
        )

    assert response.status_code == 422

def test_search_router_rejects_limit_above_maximum():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "limit": 101,
            },
        )

    assert response.status_code == 422