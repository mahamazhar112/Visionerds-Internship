from vector_store import (
    load_collection,
    is_document_indexed,
    retrieve_chunks
)
from llm import get_llm_response


def main():

    # Load existing ChromaDB collection
    load_collection()

    # Check if database exists
    if not is_document_indexed():
        print("Database not found.")
        print("Run embed.py first to generate embeddings.")
        return

    print("Database loaded successfully.")
    print("RAG Chatbot Ready.\n")

    while True:

        question = input("Ask a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Retrieve relevant chunks
        results = retrieve_chunks(question)

        retrieved_chunks = results["documents"][0]
        distances = results["distances"][0]

        print("\nRetrieved Chunks")
        print("=" * 70)

        for i, (chunk, distance) in enumerate(zip(retrieved_chunks, distances), start=1):

            print(f"\nChunk {i}")
            print("-" * 70)
            print(chunk)
            print(f"\nDistance Score: {distance:.4f}")

        # Generate answer
        answer = get_llm_response(question, retrieved_chunks)

        print("\n" + "=" * 70)
        print("Final Answer")
        print("=" * 70)
        print(answer)


if __name__ == "__main__":
    main()