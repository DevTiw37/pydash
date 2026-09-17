def build_module_endpoint(module: str) -> str:
    return f"/module/{module}"


def build_function_endpoint(module: str, name: str) -> str:
    return f"/function/{module}/{name}"


def build_class_endpoint(module: str, class_name: str) -> str:
    return f"/class/{module}/{class_name}"


def build_method_endpoint(
    module: str,
    class_name: str,
    method_name: str,
) -> str:
    return f"/method/{module}/{class_name}/{method_name}"