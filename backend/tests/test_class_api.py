from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers.class_metadata import router


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


def test_class_endpoint_returns_class_metadata():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/class/json/JSONEncoder")

    assert response.status_code == 200

    data = response.json()

    assert data["class_name"] == "JSONEncoder"
    assert isinstance(data["methods"], list)
    assert len(data["methods"]) > 0


def test_class_endpoint_returns_404_for_missing_class():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/class/json/ClassThatDoesNotExist"
        )

    assert response.status_code == 404