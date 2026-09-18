class SearchQuery:
    def normalize(self, query: str) -> str:
        query = query.strip().lower()
        query = query.replace(" ", ".")

        return query

    def split_terms(self, query: str) -> list[str]:
        query = query.strip().lower()

        return query.replace(".", " ").split()
