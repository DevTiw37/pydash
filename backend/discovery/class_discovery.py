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

    for name in dir(class_object):
        if name.startswith("_"):
            continue

        attribute = getattr(class_object, name)

        if inspect.isfunction(attribute) or inspect.isbuiltin(attribute):
            methods.append(
                DiscoveredObject(
                    name=name,
                    kind="method",
                )
            )

    methods.sort(key=lambda item: item.name)

    return methods


if __name__ == "__main__":
    from datetime import datetime

    result = discover_methods(datetime)

    print(result)