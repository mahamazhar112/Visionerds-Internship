from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

user_input = input("Enter text: ")


response = client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
    messages=[
        {
            "role": "system",
            "content": """
You are an information extraction assistant.

Extract the following fields from the user's message:

- name
- city
- age
- profession

Rules:
1. Return ONLY valid JSON.
2. Do not add any explanation.
3. Do not use Markdown.
4. Format the JSON with proper indentation.
5. If any field is missing, return null.
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)


print("\nExtracted Information:\n")
print(response.choices[0].message.content)