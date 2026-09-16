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

def split_signature_parameters(text: str):
    text = text.strip()

    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]

    parts = []
    current = []
    depth = 0

    for char in text:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1

        if char == "," and depth == 0:
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
        else:
            current.append(char)

    part = "".join(current).strip()
    if part:
        parts.append(part)

    return parts


def parse_text_signature(text: str):
    parameters = []
    kind = "POSITIONAL_ONLY"

    for part in split_signature_parameters(text):
        if part in {"$self", "$type"}:
            continue

        if part == "/":
            kind = "POSITIONAL_OR_KEYWORD"
            continue

        if part == "*":
            kind = "KEYWORD_ONLY"
            continue

        if "=" in part:
            name, default = part.split("=", 1)
        else:
            name = part
            default = None

        parameters.append(
            {
                "name": name.strip(),
                "default": default.strip() if default else None,
                "kind": kind,
            }
        )

    return parameters

def get_text_signature_parameters(function):
    text_signature = getattr(function, "__text_signature__", None)

    if not text_signature:
        return []

    return parse_text_signature(text_signature)

def get_signature(function):
    try:
        return inspect.signature(function)
    except (TypeError, ValueError):
        return None


def extract_parameters(function):
    signature = get_signature(function)

    if signature is not None:
        descriptions = extract_parameter_descriptions(function)
        parameters = []

        for parameter in signature.parameters.values():
            required = parameter.default is inspect.Parameter.empty

            parameter_info = {
                "name": parameter.name,
                "description": descriptions.get(parameter.name),
                "type": get_type_name(parameter.annotation),
                "default": None,
                "default_known": False,
                "required": required,
                "kind": parameter.kind.name,
            }

            if parameter.default is not inspect.Parameter.empty:
                parameter_info["default"] = parameter.default
                parameter_info["default_known"] = True

            parameters.append(parameter_info)

        return parameters

    text_parameters = get_text_signature_parameters(function)

    parameters = []

    for parameter in text_parameters:
        default = parameter["default"]
        has_default = default is not None

        parameters.append(
            {
                "name": parameter["name"],
                "description": None,
                "type": None,
                "default": (
                    None
                    if default == "unchanged"
                    else parse_default_value(default)
                ),
                "default_known": (
                    default != "unchanged"
                ),
                "required": not has_default,
                "kind": parameter["kind"],
            }
        )

    return parameters


def parse_default_value(value: str):
    value = value.strip()

    if value == "None":
        return None

    if value == "True":
        return True

    if value == "False":
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


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
    signature = get_signature(function)

    if signature is None:
        return None

    if signature.return_annotation is inspect.Signature.empty:
        return None

    return get_type_name(signature.return_annotation)
