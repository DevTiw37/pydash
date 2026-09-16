import importlib
import inspect

from griffe import Docstring
from typing import get_origin

def example(
    name: str,
    age: int = 20,
    active: bool = True
) -> dict:
    """
    Create an example user.

    Args:
        name: Name of the user.
        age: Age of the user.
        active: Whether the user is active.

    Returns:
        A dictionary containing the user information.
    """
    return {
        "name": name,
        "age": age,
        "active": active,
    }
    


def load_callable(module_name: str, function_name: str):
    module = importlib.import_module(module_name)

    if not hasattr(module, function_name):
        raise AttributeError(
            f"Function '{function_name}' not found in module '{module_name}'"
        )

    function = getattr(module, function_name)

    if not callable(function):
        raise TypeError(
            f"'{function_name}' is not callable"
        )

    return function


def extract_parameters(function):
    signature = inspect.signature(function)
    descriptions = extract_parameter_descriptions(function)

    parameters = []

    for parameter in signature.parameters.values():
        required = parameter.default is inspect.Parameter.empty

        parameter_info = {
            "name": parameter.name,
            "description": descriptions.get(parameter.name),
            "type": get_type_name(parameter.annotation),
            "default": None,
            "required": required,
            "kind": parameter.kind.name,
        }

        if parameter.annotation is not inspect.Parameter.empty:
            parameter_info["type"] = get_type_name(parameter.annotation)

        if parameter.default is not inspect.Parameter.empty:
            parameter_info["default"] = parameter.default

        parameters.append(parameter_info)

    return parameters


def get_type_name(annotation):
    if annotation is inspect.Parameter.empty:
        return None

    origin = get_origin(annotation)

    if origin is not None:
        return str(annotation)

    if hasattr(annotation, "__name__"):
        return annotation.__name__

    return str(annotation)


def get_docstring(function):
    return inspect.getdoc(function)

def extract_metadata(function):
    return {
        "name": function.__name__,
        "docstring": get_docstring(function),
        "return_type": get_return_type(function),
        "parameters": extract_parameters(function),
    }
    
def parse_docstring(function):
    docstring = inspect.getdoc(function)

    if not docstring:
        return None

    parsed = Docstring(
        docstring,
        parser="google"
    )

    parsed.parse()

    return parsed

def extract_parameter_descriptions(function):
    parsed = parse_docstring(function)

    descriptions = {}

    if parsed is None:
        return descriptions

    for section in parsed.parsed:
        if type(section).__name__ == "DocstringSectionParameters":
            for item in section.value:
                descriptions[item.name] = item.description

    return descriptions

def get_return_type(function):
    signature = inspect.signature(function)

    if signature.return_annotation is inspect.Signature.empty:
        return None

    return get_type_name(signature.return_annotation)

