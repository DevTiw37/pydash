from metadata.extractor import extract_metadata, load_callable


def get_function_metadata(
    module: str,
    name: str,
):
    function = load_callable(module, name)

    return extract_metadata(function)