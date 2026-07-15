from openai import OpenAI
from dotenv import load_dotenv
from config import SYSTEM_PROMPT
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

print("Hi, i am political chatbot. You can ask any questions about politics. Chatbot started! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input.strip():
        print("Please ask questions about politics:\n")
        continue

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        print("\nBot:")
        print(response.choices[0].message.content)
        print()

    except Exception as e:
        print("\nAn error occurred.")
        print(e)
        print()