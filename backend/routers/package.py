from fastapi import APIRouter, HTTPException

from models.schemas import PackageMetadata
from services.package_service import get_package_metadata


router = APIRouter(tags=["package"])


@router.get(
    "/package/{package}",
    response_model=PackageMetadata,
)
def get_package_metadata_endpoint(package: str):
    try:
        return get_package_metadata(package)
    except (ModuleNotFoundError, TypeError) as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )