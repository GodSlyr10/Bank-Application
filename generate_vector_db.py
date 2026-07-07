import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def main():
    print("Loading local bank knowledge files...")
    # Ensure source directory exists
    if not os.path.exists('./bank_knowledge'):
        print("Error: './bank_knowledge' directory not found.")
        return

    loader = DirectoryLoader('./bank_knowledge', glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("No documents found to ingest.")
        return

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    print(f"Split documents into {len(docs)} chunks.")

    # Initialize local embeddings model
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create and persist vector database to a local folder
    print("Generating embeddings and saving to disk...")
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        collection_name="bank_policy_db",
        persist_directory="./chroma_db"  # Path where database is saved
    )
    print("Vector database successfully built and stored in './chroma_db'!")

if __name__ == "__main__":
    main()
