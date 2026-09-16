from typing import Any

from pydantic import BaseModel


class ParameterMetadata(BaseModel):
    name: str
    description: str | None
    type: str | None
    default: Any | None
    default_known: bool
    required: bool
    kind: str

class FunctionMetadata(BaseModel):
    name: str
    qualified_name: str
    callable_type: str
    docstring: str | None
    return_type: str | None
    return_description: str | None
    receiver_parameter: str | None
    parameters: list[ParameterMetadata]

class MethodMetadata(FunctionMetadata):
    method_type: str


class DiscoveredObject(BaseModel):
    name: str
    kind: str


class ModuleMetadata(BaseModel):
    module: str
    callables: list[DiscoveredObject]


class ClassMetadata(BaseModel):
    class_name: str
    methods: list[DiscoveredObject]


class PackageMetadata(BaseModel):
    package: str
    modules: list[DiscoveredObject]