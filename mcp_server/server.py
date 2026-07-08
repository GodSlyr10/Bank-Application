import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from mcp.server.fastmcp import FastMCP

from vectorstore import VectorStoreManager
from services.rag_service import RAGService
from services.internet_service import InternetService



# -----------------------------
# Dependency initialization
# -----------------------------

vector_store = VectorStoreManager()

rag_service = RAGService(
    vector_store.retriever
)

internet_service = InternetService()

# -----------------------------
# MCP Server
# -----------------------------

mcp = FastMCP(
    "Bank Governance Server"
)


# -----------------------------
# MCP Tools
# -----------------------------

@mcp.tool()
def query_bank_internal_docs(query: str) -> str:
    """
    Search authoritative bank policies.

    Use for:
    - compliance
    - permissions
    - approved services
    - security controls
    - governance decisions
    """

    return rag_service.search(query)

@mcp.tool()
def search_the_public_internet(query: str) -> str:
    """
    Search public internet for technical documentation.

    Use only for:
    - GCP documentation
    - Terraform
    - APIs
    - implementation examples

    Never use for bank policy decisions.
    """

    return internet_service.search(query)

# -----------------------------
# Start server
# -----------------------------

if __name__ == "__main__":
    mcp.run()