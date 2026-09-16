def get_function_qualified_name(
    module: str,
    name: str,
) -> str:
    return f"{module}.{name}"


def get_class_qualified_name(
    module: str,
    class_name: str,
) -> str:
    return f"{module}.{class_name}"


def get_method_qualified_name(
    module: str,
    class_name: str,
    method_name: str,
) -> str:
    return f"{module}.{class_name}.{method_name}"