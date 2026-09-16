from models.search import SearchResult


SEARCH_INDEX = [
    SearchResult(
        name="datetime",
        qualified_name="datetime",
        kind="module",
    ),
    SearchResult(
        name="datetime",
        qualified_name="datetime.datetime",
        kind="class",
    ),
    SearchResult(
        name="MIMEText",
        qualified_name="email.mime.text.MIMEText",
        kind="class",
    ),
    SearchResult(
        name="as_string",
        qualified_name="email.mime.text.MIMEText.as_string",
        kind="instance_method",
    ),
]

def get_search_score(
    item: SearchResult,
    query: str,
) -> int:
    query = query.lower()
    name = item.name.lower()
    qualified_name = item.qualified_name.lower()

    if name == query:
        return 100

    if name.startswith(query):
        return 80

    if qualified_name.endswith(query):
        return 70

    if query in name or query in qualified_name:
        return 50

    return 0


def search(query: str) -> list[SearchResult]:
    query = query.strip().lower()

    if not query:
        return []

    scored_results = []

    for item in SEARCH_INDEX:
        score = get_search_score(item, query)

        if score > 0:
            scored_results.append((score, item))

    scored_results.sort(
        key=lambda result: result[0],
        reverse=True,
    )

    return [
        item
        for score, item in scored_results
    ]