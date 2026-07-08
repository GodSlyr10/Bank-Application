class RAGService:

    def __init__(self, retriever):
        self.retriever = retriever

    def search(self, query: str) -> str:
        results = self.retriever.invoke(query)

        if not results:
            return "No relevant internal bank policy found."

        return "\n---\n".join(
            doc.page_content
            for doc in results
        )