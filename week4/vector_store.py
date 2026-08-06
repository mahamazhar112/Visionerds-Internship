import os
import chromadb
from embeddings import generate_embeddings

# Anchor chroma_db path to this file's location, not the caller's cwd
CHROMA_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")


def load_collection():
    """
    Creates or loads the ChromaDB collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(
        name="book_notes"
    )
    return collection


# Load the collection once
collection = load_collection()


def is_document_indexed():
    return collection.count() > 0


def store_chunks(chunks):
    if is_document_indexed():
        print("Document already indexed.")
        return

    embeddings = generate_embeddings(chunks)

    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    print(f"{len(chunks)} chunks stored successfully.")


def retrieve_chunks(query, top_k=5):
    query_embedding = generate_embeddings([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=["documents", "distances"]
    )

    return results