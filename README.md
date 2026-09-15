# PyDash

PyDash is a developer tool for exploring Python libraries,
inspecting function metadata, and eventually generating
interactive interfaces and executable Python code.

## Current Features

- FastAPI backend
- Dynamic Python callable loading
- Function signature inspection
- Type and default value extraction
- Required parameter detection
- Parameter kind detection
- Docstring parsing
- Pydantic API schemas
- Service layer architecture

## Current API

### Health

GET `/health`

### Function Metadata

GET `/function/{package}/{module}/{name}`

Example:

`/function/math/math/pow`

## Tech Stack

- Python
- FastAPI
- Pydantic
- Griffe

## Status

🚧 PyDash is currently under active development.
