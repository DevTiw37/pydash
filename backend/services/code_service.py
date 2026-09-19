from models.code import CodeArgument, CodeRequest, CodeResponse


def format_literal(value):
    if isinstance(value, str):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'

    if isinstance(value, list):
        items = ", ".join(format_literal(item) for item in value)
        return f"[{items}]"

    if isinstance(value, tuple):
        items = ", ".join(format_literal(item) for item in value)
        if len(value) == 1:
            items += ","
        return f"({items})"

    if isinstance(value, dict):
        items = ", ".join(
            f"{format_literal(key)}: {format_literal(item)}"
            for key, item in value.items()
        )
        return f"{{{items}}}"

    return repr(value)


def format_argument(argument: CodeArgument) -> str:
    value = argument.value

    if value.expression:
        formatted_value = str(value.value)
    else:
        formatted_value = format_literal(value.value)

    if argument.positional:
        return formatted_value

    return f"{argument.name}={formatted_value}"


def generate_code(request: CodeRequest) -> CodeResponse:
    arguments = [
        format_argument(argument)
        for argument in request.arguments
    ]

    arguments_text = ", ".join(arguments)

    code = f"{request.module}.{request.name}({arguments_text})"

    return CodeResponse(code=code)