from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import get_module_metadata_endpoint


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.get(
        "/module/{module}",
    )(get_module_metadata_endpoint)
    return app


def test_module_endpoint_returns_module_metadata():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/module/json")

    assert response.status_code == 200

    data = response.json()

    assert data["module"] == "json"
    assert isinstance(data["callables"], list)
    assert len(data["callables"]) > 0

def test_module_endpoint_returns_404_for_missing_module():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/module/module_that_does_not_exist")

    assert response.status_code == 404
