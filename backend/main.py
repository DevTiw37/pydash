from fastapi import FastAPI
from contextlib import asynccontextmanager

from config import PACKAGES_TO_INDEX
from search.index_manager import search_index

from routers.search import router as search_router
from routers.function import router as function_router
from routers.module import router as module_router
from routers.class_metadata import router as class_router
from routers.method import router as method_router
from routers.package import router as package_router
from routers.code import router as code_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    search_index.rebuild(PACKAGES_TO_INDEX)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(search_router)
app.include_router(function_router)
app.include_router(module_router)
app.include_router(class_router)
app.include_router(method_router)
app.include_router(package_router)
app.include_router(code_router)


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
