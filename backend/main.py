from fastapi import FastAPI, HTTPException

from models.schemas import FunctionMetadata
from services.function_service import (
    get_function_metadata as fetch_function_metadata
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "PyDash API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get(
    "/function/{package}/{module}/{name}",
    response_model=FunctionMetadata,
)
def get_function_metadata_endpoint(
    package: str,
    module: str,
    name: str,
):
    try:
        return fetch_function_metadata(module, name)

    except (ModuleNotFoundError, AttributeError, TypeError) as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )