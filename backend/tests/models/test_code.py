import pytest
from models.code import CodeArgument, CodeRequest, CodeValue


def test_code_request_accepts_callable_and_arguments():
    request = CodeRequest(
        module="json",
        name="dumps",
        arguments=[
            CodeArgument(
                name="obj",
                value=CodeValue(
                    value="data",
                    expression=True,
                ),
                positional=True,
            ),
            CodeArgument(
                name="skipkeys",
                value=CodeValue(value=True),
            ),
        ],
    )

    assert request.module == "json"
    assert request.name == "dumps"

    assert request.arguments[0].name == "obj"
    assert request.arguments[0].value.value == "data"
    assert request.arguments[0].positional is True

    assert request.arguments[1].name == "skipkeys"
    assert request.arguments[1].value.value is True
    assert request.arguments[1].positional is False


def test_code_request_defaults_to_empty_arguments():
    request = CodeRequest(
        module="json",
        name="dumps",
    )

    assert request.arguments == []


def test_code_value_defaults_to_literal():
    value = CodeValue(value="hello")

    assert value.value == "hello"
    assert value.expression is False


def test_code_value_can_represent_expression():
    value = CodeValue(
        value="data",
        expression=True,
    )

    assert value.value == "data"
    assert value.expression is True


def test_code_argument_can_represent_positional_argument():
    argument = CodeArgument(
        name="obj",
        value=CodeValue(
            value="data",
            expression=True,
        ),
        positional=True,
    )

    assert argument.name == "obj"
    assert argument.positional is True

def test_keyword_argument_requires_name():
    with pytest.raises(ValueError, match="Keyword arguments must have a name"):
        CodeArgument(
            name=None,
            value=CodeValue(value=True),
            positional=False,
        )

def test_positional_argument_can_have_no_name():
    argument = CodeArgument(
        name=None,
        value=CodeValue(
            value="data",
            expression=True,
        ),
        positional=True,
    )

    assert argument.name is None
    assert argument.positional is True