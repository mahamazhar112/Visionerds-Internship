from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def build_rewrite_prompt(chat_history, question):
    """
    Builds a prompt to rewrite follow-up questions into standalone questions.
    Uses only previous USER questions as context.
    """

    history = ""

    # Collect only previous user questions
    user_questions = [
        message["content"]
        for message in chat_history
        if message["role"] == "user"
    ]

    # Keep only the last 3 user questions
    for previous_question in user_questions[-3:]:
        history += f"User: {previous_question}\n"

    prompt = f"""
You are a deterministic query rewriting engine for a Retrieval-Augmented Generation (RAG) system.

Your ONLY task is to rewrite the user's latest question into a standalone question.

STRICT RULES:

1. DO NOT answer the question.
2. DO NOT explain anything.
3. DO NOT summarize anything.
4. DO NOT invent information.
5. DO NOT guess missing information.
6. Preserve ALL technical terms exactly.
7. Preserve names, numbers, chapter numbers, mathematical concepts, book titles, and entities exactly.
8. ONLY resolve references like:
   - it
   - this
   - that
   - they
   - them
   - he
   - she
   - the first one
   - the second one
   - the previous chapter
9. If the latest question already makes sense on its own, return it EXACTLY as written.
10. If there is not enough context to rewrite confidently, return the original question unchanged.
11. Return ONLY the rewritten question.

Examples:

Conversation:
User: What is an eigenvalue?

Latest Question:
Why is it important?

Output:
Why is an eigenvalue important?

-------------------------

Conversation:
User: What is Chapter 1 about?

Latest Question:
What about Chapter 2?

Output:
What is Chapter 2 about?

-------------------------

Conversation:
User: What is a determinant?

Latest Question:
Can you give an example?

Output:
Can you give an example of a determinant?

-------------------------

Conversation:
User: Who wrote the book?

Latest Question:
Tell me more about the first author.

Output:
Tell me more about the first author of the book.

-------------------------

Conversation History:
{history}

Latest Question:
{question}

Standalone Question:
"""

    return prompt


def ask_groq(prompt):
    """
    Sends the rewrite prompt to Groq.
    """

    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a deterministic query rewriting engine. "
                    "Rewrite follow-up questions into standalone questions. "
                    "Never answer questions. "
                    "Never summarize. "
                    "Never invent information. "
                    "Preserve technical terms exactly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        top_p=0.1
    )

    return response.choices[0].message.content.strip()


def ask_openrouter(prompt):
    """
    Fallback to OpenRouter.
    """

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a deterministic query rewriting engine. "
                    "Rewrite follow-up questions into standalone questions. "
                    "Never answer questions. "
                    "Never summarize. "
                    "Never invent information. "
                    "Preserve technical terms exactly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        top_p=0.1
    )

    return response.choices[0].message.content.strip()


def rewrite_query(chat_history, question):
    """
    Rewrites the latest user question into a standalone question.
    """

    if len(chat_history) == 0:
        return question

    prompt = build_rewrite_prompt(chat_history, question)

    try:
        print("\nRewriting query using Groq...\n")
        rewritten = ask_groq(prompt)
        return rewritten.strip()

    except Exception as e:
        print(f"Groq failed: {e}")
        print("Trying OpenRouter...\n")

        try:
            rewritten = ask_openrouter(prompt)
            return rewritten.strip()

        except Exception as e:
            print(f"OpenRouter failed: {e}")
            print("Using original question.\n")
            return question