from fastapi import APIRouter, HTTPException

from models.schemas import FunctionMetadata
from services.function_service import (
    get_function_metadata as fetch_function_metadata,
)

router = APIRouter(
    tags=["function"],
)


@router.get(
    "/function/{module}/{name}",
    response_model=FunctionMetadata,
)
def get_function_metadata_endpoint(
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
