from fastapi import APIRouter, HTTPException

from models.schemas import ClassMetadata
from services.class_service import get_class_metadata

router = APIRouter(
    tags=["class"],
)


@router.get(
    "/class/{module}/{class_name}",
    response_model=ClassMetadata,
)
def get_class_metadata_endpoint(
    module: str,
    class_name: str,
):
    try:
        return get_class_metadata(module, class_name)

    except (ModuleNotFoundError, AttributeError) as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )