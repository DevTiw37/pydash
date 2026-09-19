from models.code import CodeArgument, CodeRequest, CodeValue
from services.code_service import generate_code


def test_generate_code_generates_function_call_with_literal_arguments():
    request = CodeRequest(
        module="json",
        name="dumps",
        arguments=[
            CodeArgument(
                name="obj",
                value=CodeValue(value="hello"),
            ),
            CodeArgument(
                name="skipkeys",
                value=CodeValue(value=True),
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == (
        'json.dumps(obj="hello", skipkeys=True)'
    )


def test_generate_code_formats_none():
    request = CodeRequest(
        module="example",
        name="function",
        arguments=[
            CodeArgument(
                name="value",
                value=CodeValue(value=None),
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == "example.function(value=None)"


def test_generate_code_formats_numbers():
    request = CodeRequest(
        module="example",
        name="function",
        arguments=[
            CodeArgument(
                name="integer",
                value=CodeValue(value=42),
            ),
            CodeArgument(
                name="decimal",
                value=CodeValue(value=3.14),
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == (
        "example.function(integer=42, decimal=3.14)"
    )


def test_generate_code_formats_collections():
    request = CodeRequest(
        module="example",
        name="function",
        arguments=[
            CodeArgument(
                name="items",
                value=CodeValue(value=[1, 2, 3]),
            ),
            CodeArgument(
                name="config",
                value=CodeValue(value={"enabled": True}),
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == (
        'example.function(items=[1, 2, 3], config={"enabled": True})'
    )


def test_generate_code_escapes_string_quotes():
    request = CodeRequest(
        module="example",
        name="function",
        arguments=[
            CodeArgument(
                name="message",
                value=CodeValue(value='say "hello"'),
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == (
        'example.function(message="say \\"hello\\"")'
    )


def test_generate_code_preserves_expression_values():
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
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == "json.dumps(obj=data)"


def test_generate_code_preserves_multiple_expression_values():
    request = CodeRequest(
        module="example",
        name="function",
        arguments=[
            CodeArgument(
                name="data",
                value=CodeValue(
                    value="user['name']",
                    expression=True,
                ),
            ),
            CodeArgument(
                name="items",
                value=CodeValue(
                    value="items[0]",
                    expression=True,
                ),
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == (
        "example.function(data=user['name'], items=items[0])"
    )

def test_generate_code_formats_positional_argument():
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
        ],
    )

    response = generate_code(request)

    assert response.code == "json.dumps(data)"

def test_generate_code_formats_mixed_positional_and_keyword_arguments():
    request = CodeRequest(
        module="example",
        name="function",
        arguments=[
            CodeArgument(
                name="data",
                value=CodeValue(
                    value="items",
                    expression=True,
                ),
                positional=True,
            ),
            CodeArgument(
                name="limit",
                value=CodeValue(value=10),
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == "example.function(items, limit=10)"

def test_generate_code_formats_positional_argument_without_name():
    request = CodeRequest(
        module="json",
        name="dumps",
        arguments=[
            CodeArgument(
                name=None,
                value=CodeValue(
                    value="data",
                    expression=True,
                ),
                positional=True,
            ),
        ],
    )

    response = generate_code(request)

    assert response.code == "json.dumps(data)"