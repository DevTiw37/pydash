from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from models.schemas import (
    FunctionMetadata,
    MethodMetadata,
    ModuleMetadata,
    ClassMetadata,
    PackageMetadata,
)
from services.function_service import (
    get_function_metadata as fetch_function_metadata
)
from services.module_service import get_module_metadata
from services.class_service import get_class_metadata
from services.method_service import get_method_metadata
from services.package_service import get_package_metadata
from config import PACKAGES_TO_INDEX
from search.index_manager import search_index
from routers.search import router as search_router
from routers.function import router as function_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    search_index.rebuild(PACKAGES_TO_INDEX)

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(search_router)
app.include_router(function_router)

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

@app.get(
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
        raise HTTPException(status_code=404, detail=str(error))
    
@app.get(
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
        
@app.get(
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
