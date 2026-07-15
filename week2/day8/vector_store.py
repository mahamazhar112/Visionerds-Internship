import chromadb

from day7.pdf_reader import read_pdf
from day7.chunker import split_into_chunks
from day7.embeddings import generate_embeddings

# Create ChromaDB client
client = chromadb.Client()

# Create collection
collection = client.create_collection("museum_notes")


def store_pdf(pdf_path):
    """
    Reads the PDF, splits it into chunks,
    generates embeddings and stores them in ChromaDB.
    """

    # Read PDF
    text = read_pdf(pdf_path)

    # Split into chunks
    chunks = split_into_chunks(text)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Store in ChromaDB
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

    print(f"{len(chunks)} chunks stored successfully!")


def search(query, top_k=3):
    """
    Retrieves the top-k most relevant chunks
    along with their distance scores.
    """

    # Generate embedding for the query
    query_embedding = generate_embeddings([query])

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=["documents", "distances"]
    )

    return results