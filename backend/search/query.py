class SearchQuery:
    def normalize(self, query: str) -> str:
        query = query.strip().lower()

        terms = query.replace(".", " ").split()

        return ".".join(terms)

    def split_terms(self, query: str) -> list[str]:
        query = query.strip().lower()

        return query.replace(".", " ").split()
