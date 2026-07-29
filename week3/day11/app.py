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

st.title("Memory Chatbot")
st.write("Ask me anything: ")

# -----------------------------
# Initialize chat history
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Display previous conversation
# -----------------------------
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("Ask a question...")

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Store user message
    st.session_state.history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Assistant response
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
                    }
                ] + st.session_state.history,
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response)

            # Store assistant response
            st.session_state.history.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")

# -----------------------------
# Statistics
# -----------------------------
total_words = sum(
    len(message["content"].split())
    for message in st.session_state.history
)

estimated_tokens = int(total_words * 1.3)

st.divider()
st.write(f"**Messages Stored:** {len(st.session_state.history)}")
st.write(f"**Estimated Tokens:** {estimated_tokens}")