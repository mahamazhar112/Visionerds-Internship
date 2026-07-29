import chromadb
from embeddings import generate_embeddings


def load_collection():
    """
    Creates or loads the ChromaDB collection.
    """
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="book_notes"
    )
    return collection


# Load the collection once
collection = load_collection()


def is_document_indexed():
    """
    Returns True if the collection already contains vectors.
    """
    return collection.count() > 0


def store_chunks(chunks):
    """
    Generates embeddings and stores them in ChromaDB.
    """

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
    """
    Retrieves the most relevant chunks for the given query.
    """

    query_embedding = generate_embeddings([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=["documents", "distances"]
    )

    return results