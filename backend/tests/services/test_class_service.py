from services.class_service import get_class_metadata


def test_get_class_metadata_returns_class_metadata():
    metadata = get_class_metadata(
        "json",
        "JSONEncoder",
    )

    assert metadata["class_name"] == "JSONEncoder"
    assert isinstance(metadata["methods"], list)
    assert len(metadata["methods"]) > 0