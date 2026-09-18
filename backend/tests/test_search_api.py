from fastapi.testclient import TestClient

from main import app


def test_search_returns_results():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={"q": "dump"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["query"] == "dump"
        assert len(data["results"]) > 0

        first_result = data["results"][0]
        
        assert first_result["name"] == "dump"
        assert first_result["qualified_name"] == "json.dump"
        assert first_result["kind"] == "function"
        assert first_result["module"] == "json"
        assert first_result["endpoint"] == "/function/json/dump"

def test_search_returns_ranked_results():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={"q": "dump"},
        )

        assert response.status_code == 200

        results = response.json()["results"]

        assert results[0]["qualified_name"] == "json.dump"
        assert results[1]["qualified_name"] == "json.dumps"

def test_search_filters_by_kind():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "kind": "function",
            },
        )

        assert response.status_code == 200

        results = response.json()["results"]

        assert len(results) == 2
        assert all(
            result["kind"] == "function"
            for result in results
        )

def test_search_rejects_invalid_kind():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "kind": "invalid",
            },
        )

        assert response.status_code == 422

def test_search_requires_query():
    with TestClient(app) as client:
        response = client.get("/search")

        assert response.status_code == 422

def test_search_rejects_empty_query():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={"q": ""},
        )

        assert response.status_code == 422

def test_search_rejects_zero_limit():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "limit": 0,
            },
        )

        assert response.status_code == 422

def test_search_rejects_limit_above_maximum():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "dump",
                "limit": 101,
            },
        )

        assert response.status_code == 422

def test_search_respects_limit():
    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "q": "json",
                "limit": 5,
            },
        )

        assert response.status_code == 200

        results = response.json()["results"]

        assert len(results) == 5

