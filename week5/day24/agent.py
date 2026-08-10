import sys
import os
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time

from openai import OpenAI, BadRequestError
from dotenv import load_dotenv

from tools import tools, calculator, wordcount, document_lookup
from vector_store import load_collection

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

available_functions = {
    "calculator": calculator,
    "wordcount": wordcount,
    "document_lookup": document_lookup
}

MAX_TOOL_CALL_RETRIES = 5


def call_with_tool_retry(messages):
    last_error = None
    for attempt in range(1, MAX_TOOL_CALL_RETRIES + 1):
        try:
            return client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0 if attempt == 1 else 0.3  # vary temperature on retries so it isn't the exact same failure
            )
        except BadRequestError as e:
            last_error = e
            if "tool_use_failed" in str(e):
                print(f"[Retry {attempt}/{MAX_TOOL_CALL_RETRIES}] Tool call generation failed, retrying...")
                time.sleep(1)
                continue
            raise
    raise last_error


def run_agent(user_question, history=None):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. You have access to EXACTLY three tools: "
                "calculator, wordcount, document_lookup. No other tools exist. "
                "Never attempt to call any tool other than these three.\n\n"
                "Decision rule, follow it exactly:\n"
                "1. If the question is about math/arithmetic, call ONLY calculator.\n"
                "2. If the question asks to count words in a given text, call ONLY wordcount.\n"
                "3. If the question is about linear algebra or the textbook content, "
                "call ONLY document_lookup. Do not answer these from your own knowledge.\n"
                "4. For anything else, do NOT call any tool — answer directly in plain text.\n\n"
                "If one tool call isn't enough to fully answer the question (for example, "
                "you need to look something up before you can calculate with it), you may "
                "call another tool after seeing the first result.\n\n"
                "If the question asks you to calculate something (like a determinant, "
                "inverse, or eigenvalue of a specific matrix) but the calculator tool can only "
                "do basic add/subtract/multiply/divide on two numbers, and no specific matrix "
                "values were given, do NOT attempt to force the calculator to solve it. Instead, "
                "explain directly in plain text that this calculation is outside the current "
                "tool's capability.\n\n"
                "Formatting rule: if you call a tool, your entire response must be ONLY the "
                "tool call, no explanatory text. If not calling a tool, respond in plain text only."
            )
        }
    ]

    # Insert past conversation turns (if any) before the current question
    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": user_question})

    step_number = 1
    MAX_STEPS = 5

    while step_number <= MAX_STEPS:

        # ---- REASON ----
        print(f"\n{'='*50}")
        print(f"STEP {step_number} — REASON")
        print(f"{'='*50}")
        print("Thinking about whether a tool is needed...")

        try:
            response = call_with_tool_retry(messages)
        except BadRequestError:
            print("Tool call generation failed after all retries.")
            return "I had trouble processing that request. Could you try rephrasing it?"

        response_message = response.choices[0].message

        if not response_message.tool_calls:
            print("Decision: No tool needed. Answering directly.")
            return response_message.content

        messages.append(response_message)

        # ---- ACT ----
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"\nSTEP {step_number} — ACT")
            print(f"Decision: call tool -> {function_name}({function_args})")

            function_to_call = available_functions[function_name]
            function_result = function_to_call(**function_args)

            # ---- OBSERVE ----
            print(f"\nSTEP {step_number} — OBSERVE")
            print(f"Result received: {str(function_result)[:200]}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(function_result)
            })

        step_number += 1

        if step_number > MAX_STEPS:
            break

        messages.append({
            "role": "system",
            "content": (
                "You now have the tool result(s) above. If you have everything you need, "
                "write the final answer as a complete, natural-language sentence — do NOT "
                "call any tool in this case. If you still need another tool call to fully "
                "answer the original question, call the appropriate tool now instead."
            )
        })

        try:
            next_response = call_with_tool_retry(messages)
        except BadRequestError:
            print("Tool call generation failed after all retries.")
            return "I had trouble processing that request. Could you try rephrasing it?"

        next_message = next_response.choices[0].message

        if not next_message.tool_calls:
            print(f"\n{'='*50}")
            print(f"STEP {step_number} — REASON")
            print(f"{'='*50}")
            print("Decision: Have enough information. Producing final answer.")
            return next_message.content

        messages.append(next_message)
        response_message = next_message

        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"\nSTEP {step_number} — ACT")
            print(f"Decision: call tool -> {function_name}({function_args})")

            function_to_call = available_functions[function_name]
            function_result = function_to_call(**function_args)

            print(f"\nSTEP {step_number} — OBSERVE")
            print(f"Result received: {str(function_result)[:200]}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(function_result)
            })

        step_number += 1

    # Safety net: loop hit MAX_STEPS without reaching a final answer
    print(f"\n{'='*50}")
    print("MAX STEPS REACHED — stopping to avoid an infinite loop")
    print(f"{'='*50}")
    return "I wasn't able to fully answer this using the available tools."


def main():
    load_collection()
    print("Agent ready (Day 24 — with history support). Type 'exit' to quit.\n")

    history = []
    while True:
        question = input("Ask something: ").strip()
        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = run_agent(question, history=history)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})

        print(f"\n{'='*50}")
        print("FINAL ANSWER")
        print(f"{'='*50}")
        print(answer)
        print()


if __name__ == "__main__":
    main()