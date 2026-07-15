from openai import OpenAI
from dotenv import load_dotenv
from config import SYSTEM_PROMPT
import streamlit as st
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(
    page_title="Politics Chatbot",
    layout="centered"
)

st.title("Politics Chatbot")
st.write("Ask any question related to politics.")

user_input = st.chat_input("Ask a political question...")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

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
                ],
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")