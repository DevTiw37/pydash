from discovery.object_identity import get_function_qualified_name
from metadata.extractor import extract_metadata, load_callable


def get_function_metadata(module: str, name: str):
    function = load_callable(module, name)

    qualified_name = get_function_qualified_name(
        module,
        name,
    )

    return extract_metadata(
        function,
        qualified_name=qualified_name,
    )