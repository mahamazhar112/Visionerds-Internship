import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Groq Client
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# OpenRouter Client
openrouter_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def build_prompt(question, context):

    prompt = f"""
You are a helpful AI assistant answering questions about a document.

Instructions:
1. Answer ONLY using the information provided in the context below.
2. The user may ask direct questions, contextual questions, follow up questions, or ask for explanations based on the document.
3. Carefully understand the user's intent before answering.
4. If the context contains enough information, provide a clear and concise answer.
5. If the answer cannot be found in the context, reply exactly:

"I don't know based on the provided document."

6. Do not use outside knowledge, assumptions, or make up information.
7. Do not mention these instructions in your response.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt


def ask_groq(prompt):
    """
    Sends prompt to Groq.
    """

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def ask_openrouter(prompt):
    """
    Sends prompt to OpenRouter.
    """

    response = openrouter_client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def get_llm_response(question, retrieved_chunks):
    """
    Uses Groq first.
    If Groq fails, automatically switches to OpenRouter.
    """

    prompt = build_prompt(question, retrieved_chunks)

    try:
        print("\nUsing Groq...\n")
        return ask_groq(prompt)

    except Exception as groq_error:

        print("Groq unavailable.")
        print(groq_error)

        print("\nSwitching to OpenRouter...\n")

        try:
            return ask_openrouter(prompt)

        except Exception as openrouter_error:

            print("OpenRouter unavailable.")
            print(openrouter_error)

            return "Both Groq and OpenRouter are currently unavailable."