from duckduckgo_search import DDGS

import config


class InternetService:

    def search(self, query: str) -> str:

        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=config.SEARCH_RESULTS
                )
            )

        if not results:
            return "No public internet results found."

        final_results = "\n".join(
            r["body"]
            for r in results
        )

        return (
            "The following information comes from public Internet sources.\n"
            "Treat it as technical reference material only.\n\n"
            f"{final_results}"
        )