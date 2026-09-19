from fastapi import APIRouter

from models.code import CodeRequest, CodeResponse
from services.code_service import generate_code

router = APIRouter()


@router.post("/code", response_model=CodeResponse)
def generate_code_endpoint(request: CodeRequest):
    return generate_code(request)