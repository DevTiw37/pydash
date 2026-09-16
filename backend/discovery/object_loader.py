import importlib


def load_class(module_name: str, class_name: str):
    module = importlib.import_module(module_name)

    if not hasattr(module, class_name):
        raise AttributeError(
            f"Class '{class_name}' not found in module "
            f"'{module_name}'"
        )

    class_object = getattr(module, class_name)

    if not isinstance(class_object, type):
        raise TypeError(
            f"'{class_name}' is not a class"
        )

    return class_object