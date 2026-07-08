from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import config

import logging


class VectorStoreManager:

    def __init__(self):

        logging.info("Loading vector store...")

        embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL
        )

        vectorstore = Chroma(
            persist_directory=config.CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=config.COLLECTION_NAME,
        )

        self._retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": config.RETRIEVAL_K
            }
        )

    @property
    def retriever(self):
        return self._retriever