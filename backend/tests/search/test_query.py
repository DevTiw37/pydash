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