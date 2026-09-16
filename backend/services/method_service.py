from discovery.class_discovery import (
    get_method_type,
    load_method,
)
from discovery.object_loader import load_class
from metadata.extractor import extract_metadata
from discovery.object_identity import get_method_qualified_name


def get_method_metadata(
    module: str,
    class_name: str,
    method_name: str,
):
    class_object = load_class(module, class_name)

    method = load_method(class_object, method_name)

    qualified_name = get_method_qualified_name(
        module,
        class_name,
        method_name,
    )

    metadata = extract_metadata(
        method,
        callable_type="method",
        qualified_name=qualified_name,
    )

    method_type = get_method_type(
        class_object,
        method_name,
    )

    return {
        **metadata,
        "method_type": method_type,
    }