from typing import Any

from pydantic import BaseModel


class ParameterMetadata(BaseModel):
    name: str
    description: str | None
    type: str | None
    default: Any | None
    required: bool
    kind: str


class FunctionMetadata(BaseModel):
    name: str
    docstring: str | None
    return_type: str | None
    parameters: list[ParameterMetadata]

class ModuleMetadata(BaseModel):
    module: str
    callables: list[DiscoveredObject]
    
class DiscoveredObject(BaseModel):
    name: str
    kind: str
    
class ClassMetadata(BaseModel):
    class_name: str
    methods: list[DiscoveredObject]
    
class PackageMetadata(BaseModel):
    package: str
    modules: list[DiscoveredObject]