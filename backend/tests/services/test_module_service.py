from services.module_service import get_module_metadata


def test_get_module_metadata_returns_module_metadata():
    metadata = get_module_metadata("json")

    assert metadata["module"] == "json"
    assert isinstance(metadata["callables"], list)
    assert len(metadata["callables"]) > 0