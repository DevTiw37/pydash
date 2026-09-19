from datetime import datetime

from metadata.extractor import extract_metadata


def test_extract_metadata_uses_text_signature_for_builtin():
    metadata = extract_metadata(
        datetime.now,
        qualified_name="datetime.datetime.now",
    )

    assert metadata["name"] == "now"
    assert metadata["qualified_name"] == "datetime.datetime.now"

    parameters = metadata["parameters"]

    assert len(parameters) == 1
    assert parameters[0]["name"] == "tz"
    assert parameters[0]["default"] is None
    assert parameters[0]["default_known"] is True
    assert parameters[0]["required"] is False

def test_extract_metadata_returns_function_metadata():
    metadata = extract_metadata(
        lambda name, age=20: {
            "name": name,
            "age": age,
        },
        qualified_name="example.user",
    )

    assert metadata["name"] == "<lambda>"
    assert metadata["qualified_name"] == "example.user"
    assert metadata["callable_type"] == "function"
    assert metadata["receiver_parameter"] is None
    assert len(metadata["parameters"]) == 2


def test_extract_metadata_extracts_types_defaults_and_required_status():
    def create_user(
        name: str,
        age: int = 20,
        active: bool = True,
    ) -> dict:
        return {
            "name": name,
            "age": age,
            "active": active,
        }

    metadata = extract_metadata(
        create_user,
        qualified_name="example.create_user",
    )

    assert metadata["return_type"] == "dict"

    parameters = metadata["parameters"]

    assert parameters[0]["name"] == "name"
    assert parameters[0]["type"] == "str"
    assert parameters[0]["required"] is True
    assert parameters[0]["default_known"] is False

    assert parameters[1]["name"] == "age"
    assert parameters[1]["type"] == "int"
    assert parameters[1]["default"] == 20
    assert parameters[1]["default_known"] is True
    assert parameters[1]["required"] is False

    assert parameters[2]["name"] == "active"
    assert parameters[2]["type"] == "bool"
    assert parameters[2]["default"] is True
    assert parameters[2]["default_known"] is True
    assert parameters[2]["required"] is False


def test_extract_metadata_extracts_google_docstring_descriptions():
    def create_user(
        name: str,
        age: int = 20,
    ) -> dict:
        """
        Create a user.

        Args:
            name: Name of the user.
            age: Age of the user.

        Returns:
            A dictionary containing the user information.
        """
        return {
            "name": name,
            "age": age,
        }

    metadata = extract_metadata(
        create_user,
        qualified_name="example.create_user",
    )

    assert metadata["docstring"] is not None
    assert metadata["return_description"] == (
        "A dictionary containing the user information."
    )

    parameters = metadata["parameters"]

    assert parameters[0]["description"] == "Name of the user."
    assert parameters[1]["description"] == "Age of the user."

def test_extract_metadata_preserves_parameter_kinds():
    def example(
        positional_only,
        /,
        positional_or_keyword,
        *args,
        keyword_only,
        **kwargs,
    ):
        pass

    metadata = extract_metadata(
        example,
        qualified_name="example.example",
    )

    parameters = metadata["parameters"]

    assert parameters[0]["name"] == "positional_only"
    assert parameters[0]["kind"] == "POSITIONAL_ONLY"

    assert parameters[1]["name"] == "positional_or_keyword"
    assert parameters[1]["kind"] == "POSITIONAL_OR_KEYWORD"

    assert parameters[2]["name"] == "args"
    assert parameters[2]["kind"] == "VAR_POSITIONAL"

    assert parameters[3]["name"] == "keyword_only"
    assert parameters[3]["kind"] == "KEYWORD_ONLY"

    assert parameters[4]["name"] == "kwargs"
    assert parameters[4]["kind"] == "VAR_KEYWORD"