from discovery.class_discovery import discover_methods


def get_class_metadata(module: str, class_name: str):
    module_object = __import__(module, fromlist=[class_name])

    class_object = getattr(module_object, class_name)

    methods = discover_methods(class_object)

    return {
        "class_name": class_name,
        "methods": methods,
    }