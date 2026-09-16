from discovery.class_discovery import discover_methods
from discovery.object_loader import load_class


def get_class_metadata(module: str, class_name: str):
    class_object = load_class(module, class_name)

    methods = discover_methods(class_object)

    return {
        "class_name": class_name,
        "methods": methods,
    }