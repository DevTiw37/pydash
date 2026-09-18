from search.query import SearchQuery


def test_normalize_search_query():
    parser = SearchQuery()

    assert parser.normalize(" json dump ") == "json.dump"
    assert parser.normalize("JSON DUMP") == "json.dump"


def test_split_search_query():
    parser = SearchQuery()

    assert parser.split_terms("json.encoder") == ["json", "encoder"]
    assert parser.split_terms("json encoder") == ["json", "encoder"]


def test_normalize_empty_query():
    parser = SearchQuery()

    assert parser.normalize("") == ""


def test_split_empty_query():
    parser = SearchQuery()

    assert parser.split_terms("") == []

def test_normalize_multiple_spaces():
    parser = SearchQuery()

    assert parser.normalize("json   dump") == "json.dump"

def test_normalize_tabs():
    parser = SearchQuery()

    assert parser.normalize("json\tdump") == "json.dump"

def test_normalize_dot_separated_query():
    parser = SearchQuery()

    assert parser.normalize("JSON.Encoder") == "json.encoder"

def test_split_mixed_case_query():
    parser = SearchQuery()

    assert parser.split_terms("JSON.Encoder") == ["json", "encoder"]
