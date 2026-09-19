from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_generate_code_endpoint():
    response = client.post(
        "/code",
        json={
            "module": "json",
            "name": "dumps",
            "arguments": [
                {
                    "name": "obj",
                    "value": {
                        "value": "data",
                        "expression": True,
                    },
                    "positional": True,
                },
                {
                    "name": "skipkeys",
                    "value": {
                        "value": True,
                    },
                    "positional": False,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "code": "json.dumps(data, skipkeys=True)"
    }

def test_generate_code_endpoint_with_no_arguments():
    response = client.post(
        "/code",
        json={
            "module": "datetime",
            "name": "now",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "code": "datetime.now()"
    }

def test_generate_code_endpoint_with_literal_arguments():
    response = client.post(
        "/code",
        json={
            "module": "json",
            "name": "dumps",
            "arguments": [
                {
                    "name": "skipkeys",
                    "value": {
                        "value": True,
                    },
                },
                {
                    "name": "indent",
                    "value": {
                        "value": 4,
                    },
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "code": "json.dumps(skipkeys=True, indent=4)"
    }

def test_generate_code_endpoint_with_expression_argument():
    response = client.post(
        "/code",
        json={
            "module": "json",
            "name": "dumps",
            "arguments": [
                {
                    "name": "obj",
                    "value": {
                        "value": "data",
                        "expression": True,
                    },
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "code": "json.dumps(obj=data)"
    }

def test_generate_code_endpoint_rejects_invalid_arguments():
    response = client.post(
        "/code",
        json={
            "module": "json",
            "name": "dumps",
            "arguments": "invalid",
        },
    )

    assert response.status_code == 422