from vector_store import (
    load_collection,
    is_document_indexed,
    retrieve_chunks
)

from llm import get_llm_response
from rewrite import rewrite_query
from summarizer import summarize_history

TRIGGER_LENGTH = 8    # once raw history exceeds this many messages, summarize
KEEP_RECENT = 4       # always keep this many most-recent raw messages after summarizing


def main():

    # Load existing ChromaDB collection
    load_collection()

    # Check if embeddings exist
    if not is_document_indexed():
        print("Database not found.")
        print("Run embed.py first.")
        return

    print("Database loaded successfully.")
    print("Conversational RAG Chatbot Ready (Summarization Memory).\n")

    # Running summary of everything older than the recent window
    running_summary = ""

    # Raw recent messages (not yet summarized)
    chat_history = []

    while True:

        question = input("Ask a question (type 'exit' to quit): ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Build combined context for rewriting:
        # treat the summary as a synthetic prior "user" turn so rewrite_query
        # still has access to older facts, plus the recent raw turns.
        history_for_rewrite = []

        if running_summary:
            history_for_rewrite.append({
                "role": "user",
                "content": f"(Earlier conversation summary: {running_summary})"
            })

        history_for_rewrite.extend(chat_history)

        # Rewrite follow-up question
        rewritten_question = rewrite_query(history_for_rewrite, question)

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

        # If history has grown past the trigger length, summarize the older
        # portion and keep only the most recent messages as raw text.
        if len(chat_history) > TRIGGER_LENGTH:

            messages_to_compress = chat_history[:-KEEP_RECENT]
            chat_history = chat_history[-KEEP_RECENT:]

            running_summary = summarize_history(
                running_summary,
                messages_to_compress
            )

            print("\n" + "=" * 70)
            print("Updated Running Summary")
            print("=" * 70)
            print(running_summary)


if __name__ == "__main__":
    main()