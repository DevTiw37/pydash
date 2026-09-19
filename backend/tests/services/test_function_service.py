from services.function_service import get_function_metadata


def test_get_function_metadata_returns_function_metadata():
    metadata = get_function_metadata(
        "json",
        "dump",
    )

    assert metadata["name"] == "dump"
    assert metadata["qualified_name"] == "json.dump"
    assert metadata["callable_type"] == "function"
    assert isinstance(metadata["parameters"], list)