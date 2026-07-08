from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

user_input = input("Enter your text: ")

response = client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
    messages=[
        {
            "role": "system",
            "content": """
You are an expert sentiment analysis assistant.

Analyze the user's message and determine:

- sentiment
- emotion
- confidence

Rules:

1. Return ONLY valid JSON.
2. Do not add any explanation.
3. Do not use Markdown.
4. Format the JSON with proper indentation.
5. Sentiment must be one of:
   - Positive
   - Negative
   - Neutral
6. Confidence must be a decimal value between 0 and 1.
7. Emotion should be a single word such as:
   Joy
   Sadness
   Anger
   Fear
   Surprise
   Love
   Excitement
   Disgust
   None

Examples:

Example 1

Input:
I got promoted today! I'm so happy!

Output:
{
    "sentiment": "Positive",
    "emotion": "Joy",
    "confidence": 0.98
}

Example 2

Input:
I failed my final exam and I feel terrible.

Output:
{
    "sentiment": "Negative",
    "emotion": "Sadness",
    "confidence": 0.97
}

Example 3

Input:
The meeting was okay. Nothing special happened.

Output:
{
    "sentiment": "Neutral",
    "emotion": "None",
    "confidence": 0.92
}

Now analyze the user's message and return only the JSON response.
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)

print("\nSentiment Analysis:\n")
print(response.choices[0].message.content)