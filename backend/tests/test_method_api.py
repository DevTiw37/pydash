from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers.method import router


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


def test_method_endpoint_returns_method_metadata():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/method/json/JSONEncoder/encode"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "encode"
    assert data["qualified_name"] == "json.JSONEncoder.encode"
    assert data["callable_type"] == "method"
    assert data["method_type"] == "instance_method"
    assert data["receiver_parameter"] == "self"
    assert isinstance(data["parameters"], list)


def test_method_endpoint_returns_404_for_missing_method():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/method/json/JSONEncoder/method_that_does_not_exist"
        )

    assert response.status_code == 404