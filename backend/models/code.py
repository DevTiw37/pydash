from typing import Any

from pydantic import BaseModel, Field, model_validator


class CodeValue(BaseModel):
    value: Any
    expression: bool = False


class CodeArgument(BaseModel):
    name: str | None
    value: CodeValue
    positional: bool = False

    @model_validator(mode="after")
    def validate_argument(self):
        if not self.positional and self.name is None:
            raise ValueError(
                "Keyword arguments must have a name"
            )

        return self


class CodeRequest(BaseModel):
    module: str
    name: str
    arguments: list[CodeArgument] = Field(default_factory=list)


class CodeResponse(BaseModel):
    code: str