from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def build_summary_prompt(existing_summary, messages_to_compress):
    """
    Builds a prompt that compresses old conversation turns into a short summary.
    Combines with any existing summary so context isn't lost across multiple
    rounds of summarization.
    """

    conversation_text = ""

    for message in messages_to_compress:
        role = "User" if message["role"] == "user" else "Assistant"
        conversation_text += f"{role}: {message['content']}\n"

    prompt = f"""
You are a summarization engine for a conversational AI system.

Your ONLY task is to update a running summary of a conversation by incorporating
new turns into it.

STRICT RULES:

1. Preserve all important facts, names, numbers, and topics mentioned by the user.
2. Keep the summary concise — a few sentences, not a full recap.
3. Do NOT lose earlier facts that are still present in the existing summary.
4. Do NOT answer any questions from the conversation.
5. Do NOT add information that wasn't in the conversation.
6. Write the summary in third person (e.g., "The user asked about...", "The user's name is...").
7. Return ONLY the updated summary text, nothing else.

Existing Summary:
{existing_summary if existing_summary else "(none yet)"}

New Conversation Turns:
{conversation_text}

Updated Summary:
"""

    return prompt


def ask_groq(prompt):
    """
    Sends the summarization prompt to Groq.
    """

    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a summarization engine. "
                    "Compress conversation turns into a concise running summary. "
                    "Never answer questions. Never invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
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
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a summarization engine. "
                    "Compress conversation turns into a concise running summary. "
                    "Never answer questions. Never invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def summarize_history(existing_summary, messages_to_compress):
    """
    Compresses given messages into an updated summary,
    merging with any existing summary.
    """

    prompt = build_summary_prompt(existing_summary, messages_to_compress)

    try:
        print("\nSummarizing history using Groq...\n")
        return ask_groq(prompt)

    except Exception as e:
        print(f"Groq failed: {e}")
        print("Trying OpenRouter...\n")

        try:
            return ask_openrouter(prompt)

        except Exception as e:
            print(f"OpenRouter failed: {e}")
            print("Keeping existing summary unchanged.\n")
            return existing_summary