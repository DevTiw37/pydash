from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers.package import router


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


def test_package_endpoint_returns_package_metadata():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/package/json")

    assert response.status_code == 200

    data = response.json()

    assert data["package"] == "json"
    assert isinstance(data["modules"], list)
    assert len(data["modules"]) > 0


def test_package_endpoint_returns_404_for_missing_package():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/package/package_that_does_not_exist"
        )

    assert response.status_code == 404