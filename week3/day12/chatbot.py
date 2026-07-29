from vector_store import (
    load_collection,
    is_document_indexed,
    retrieve_chunks
)

from llm import get_llm_response
from rewrite import rewrite_query


def main():

    # Load existing ChromaDB collection
    load_collection()

    # Check if embeddings exist
    if not is_document_indexed():
        print("Database not found.")
        print("Run embed.py first.")
        return

    print("Database loaded successfully.")
    print("Conversational RAG Chatbot Ready.\n")

    # Store conversation history
    chat_history = []

    while True:

        question = input("Ask a question (type 'exit' to quit): ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Rewrite follow-up question
        rewritten_question = rewrite_query(chat_history, question)

        print("\nRewritten Query:")
        print(rewritten_question)

        # Retrieve relevant chunks
        results = retrieve_chunks(rewritten_question)

        retrieved_chunks = results["documents"][0]
        distances = results["distances"][0]

        print("\nRetrieved Chunks")
        print("=" * 70)

        for i, (chunk, distance) in enumerate(
            zip(retrieved_chunks, distances),
            start=1
        ):
            print(f"\nChunk {i}")
            print("-" * 70)
            print(chunk)
            print(f"\nDistance Score: {distance:.4f}")

        # Generate answer
        answer = get_llm_response(rewritten_question, retrieved_chunks)

        print("\n" + "=" * 70)
        print("Final Answer")
        print("=" * 70)
        print(answer)

        # Save conversation history
        chat_history.extend([
            {
                "role": "user",
                "content": question
            },
            {
                "role": "assistant",
                "content": answer
            }
        ])


if __name__ == "__main__":
    main()