from fastapi import APIRouter, HTTPException

from models.schemas import MethodMetadata
from services.method_service import get_method_metadata

router = APIRouter(
    tags=["method"],
)


@router.get(
    "/method/{module}/{class_name}/{method_name}",
    response_model=MethodMetadata,
)
def get_method_metadata_endpoint(
    module: str,
    class_name: str,
    method_name: str,
):
    try:
        return get_method_metadata(
            module,
            class_name,
            method_name,
        )
    except (ModuleNotFoundError, AttributeError, TypeError) as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )