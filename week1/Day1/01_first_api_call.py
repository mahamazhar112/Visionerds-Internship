from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
    messages=[
        {
            "role": "system",
            "content": "You are an experienced fitness coach."
                      
        },
        {
            "role": "user",
            "content": "how to gain weight"
        }
    ]
)

print(response.choices[0].message.content)