from typing import Any

from pydantic import BaseModel


class ParameterMetadata(BaseModel):
    name: str
    description: str | None
    type: str | None
    default: Any
    required: bool
    kind: str


class FunctionMetadata(BaseModel):
    name: str
    docstring: str | None
    return_type: str | None
    parameters: list[ParameterMetadata]