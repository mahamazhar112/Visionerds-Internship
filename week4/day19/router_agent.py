import sys
import os
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json

from openai import OpenAI
from dotenv import load_dotenv

from tools import document_lookup
from vector_store import load_collection
from agent import run_agent as run_tool_agent  # reuse Day 17's full tool-calling loop

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def classify_question(user_question):
    """
    Router step: asks the LLM to label the question as one of
    'document', 'tool', or 'conversational'. Returns the label as a string.
    """

    classification_prompt = [
        {
            "role": "system",
            "content": (
                "You are a router. Classify the user's question into EXACTLY one "
                "of these three categories. Reply with ONLY the single word label, "
                "nothing else, no punctuation, no explanation.\n\n"
                "- document: the question is about linear algebra or textbook content "
                "(matrices, vectors, eigenvalues, determinants, transformations, etc.)\n"
                "- tool: the question needs math/arithmetic calculation, or word counting\n"
                "- conversational: anything else — greetings, general knowledge, opinions, "
                "small talk, or questions unrelated to the textbook and not needing a tool\n\n"
                "Reply with only one word: document, tool, or conversational."
            )
        },
        {"role": "user", "content": user_question}
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=classification_prompt,
        temperature=0
    )

    label = response.choices[0].message.content.strip().lower()

    # safety net in case the model adds stray words/punctuation
    if "document" in label:
        return "document"
    elif "tool" in label:
        return "tool"
    else:
        return "conversational"


def handle_document(user_question):
    """
    Document path: retrieve the best matching chunk, then have the LLM
    answer using only that retrieved content.
    """
    retrieved_text = document_lookup(user_question)

    messages = [
        {
            "role": "system",
            "content": (
                "Answer the user's question using ONLY the retrieved textbook passage "
                "below. Do not use outside knowledge. Answer in a complete, natural "
                "sentence.\n\n"
                f"Retrieved passage:\n{retrieved_text}"
            )
        },
        {"role": "user", "content": user_question}
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content


def handle_conversational(user_question):
    """
    Conversational path: answer directly, no tools, no retrieval.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful, friendly assistant. Answer directly and briefly."
        },
        {"role": "user", "content": user_question}
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content


def route(user_question):
    """
    Main router entry point: classifies the question, prints the routing
    decision, then dispatches to the correct handler.
    """

    label = classify_question(user_question)

    print(f"\n[Router Decision] '{user_question}' -> {label}")

    if label == "document":
        return handle_document(user_question)
    elif label == "tool":
        return run_tool_agent(user_question)  # reuses Day 17's full ReAct loop
    else:
        return handle_conversational(user_question)


def main():
    load_collection()
    print("Router agent ready (Day 19). Type 'exit' to quit.\n")

    while True:
        question = input("Ask something: ").strip()
        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = route(question)

        print("\nFinal Answer:")
        print(answer)
        print()


if __name__ == "__main__":
    main()