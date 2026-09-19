from fastapi import APIRouter, HTTPException

from models.schemas import ModuleMetadata
from services.module_service import get_module_metadata

router = APIRouter(
    tags=["module"],
)


@router.get(
    "/module/{module}",
    response_model=ModuleMetadata,
)
def get_module_metadata_endpoint(module: str):
    try:
        return get_module_metadata(module)

    except ModuleNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
