import importlib

from discovery.class_discovery import load_method
from metadata.extractor import extract_metadata


def get_method_metadata(
    module: str,
    class_name: str,
    method_name: str,
):
    module_object = importlib.import_module(module)

    class_object = getattr(module_object, class_name)

    method = load_method(class_object, method_name)

    return extract_metadata(method)