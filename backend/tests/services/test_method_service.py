from services.method_service import get_method_metadata


def test_get_method_metadata_returns_instance_method_metadata():
    metadata = get_method_metadata(
        "json",
        "JSONEncoder",
        "encode",
    )

    assert metadata["name"] == "encode"
    assert metadata["qualified_name"] == "json.JSONEncoder.encode"
    assert metadata["callable_type"] == "method"
    assert metadata["method_type"] == "instance_method"
    assert metadata["receiver_parameter"] == "self"