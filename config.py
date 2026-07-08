CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "bank_policy_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

OLLAMA_MODEL = "qwen2.5:3b"

OLLAMA_URL = "http://localhost:11434"

SEARCH_RESULTS = 5

RETRIEVAL_K = 3

MCP_SERVERS = {

    "bank": {

        "command": "python",

        "args": [
            "mcp_server/server.py"
        ]

    }

}