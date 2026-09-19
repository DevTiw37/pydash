from services.package_service import get_package_metadata


def test_get_package_metadata_returns_package_metadata():
    metadata = get_package_metadata("json")

    assert metadata["package"] == "json"
    assert isinstance(metadata["modules"], list)
    assert len(metadata["modules"]) > 0