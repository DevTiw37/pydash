import inspect

from models.schemas import DiscoveredObject

def load_method(class_object, method_name: str):
    if not hasattr(class_object, method_name):
        raise AttributeError(
            f"Method '{method_name}' not found in class "
            f"'{class_object.__name__}'"
        )

    method = getattr(class_object, method_name)

    if not callable(method):
        raise TypeError(
            f"'{method_name}' is not callable"
        )

    return method

def discover_methods(class_object) -> list[DiscoveredObject]:
    methods: list[DiscoveredObject] = []
    discovered_names: set[str] = set()

    for current_class in class_object.__mro__:
        if current_class is object:
            continue

        for name, attribute in current_class.__dict__.items():
            if name.startswith("_"):
                continue

            if name in discovered_names:
                continue

            if isinstance(attribute, classmethod):
                kind = "class_method"

            elif isinstance(attribute, staticmethod):
                kind = "static_method"

            elif type(attribute).__name__ == "classmethod_descriptor":
                kind = "class_method"

            elif type(attribute).__name__ == "method_descriptor":
                kind = "instance_method"

            elif inspect.isfunction(attribute):
                kind = "instance_method"

            else:
                continue

            methods.append(
                DiscoveredObject(
                    name=name,
                    kind=kind,
                )
            )

            discovered_names.add(name)

    methods.sort(key=lambda item: item.name)

    return methods

def get_method_type(class_object, method_name: str) -> str:
    for current_class in class_object.__mro__:
        if current_class is object:
            continue

        if method_name not in current_class.__dict__:
            continue

        attribute = current_class.__dict__[method_name]

        if isinstance(attribute, classmethod):
            return "class_method"

        if isinstance(attribute, staticmethod):
            return "static_method"

        if type(attribute).__name__ == "classmethod_descriptor":
            return "class_method"

        if type(attribute).__name__ == "method_descriptor":
            return "instance_method"

        if inspect.isfunction(attribute):
            return "instance_method"

    raise AttributeError(
        f"Method '{method_name}' not found in class "
        f"'{class_object.__name__}'"
    )



if __name__ == "__main__":
    from datetime import datetime

    result = discover_methods(datetime)

    print(result)