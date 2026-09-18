class SearchQuery:
    def split_terms(self, query: str) -> list[str]:
        query = query.strip().lower()

        return query.replace(".", " ").split()

    def normalize(self, query: str) -> str:
        terms = self.split_terms(query)

        return ".".join(terms)