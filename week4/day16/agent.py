import os
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

# Map tool names (as strings) to the actual Python functions
available_functions = {
    "calculator": calculator,
    "wordcount": wordcount,
    "document_lookup": document_lookup
}

MAX_TOOL_CALL_RETRIES = 3


def call_with_tool_retry(messages):
    """
    Groq's tool-calling generation can occasionally return malformed JSON
    for the function arguments (a tool_use_failed 400 error). This is
    usually transient, so retry a few times before giving up.
    """
    last_error = None

    for attempt in range(1, MAX_TOOL_CALL_RETRIES + 1):
        try:
            return client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0
            )
        except BadRequestError as e:
            last_error = e
            if "tool_use_failed" in str(e):
                print(f"[Retry {attempt}/{MAX_TOOL_CALL_RETRIES}] "
                      f"Tool call generation failed, retrying...")
                time.sleep(1)
                continue
            raise  # some other kind of BadRequestError, don't swallow it

    # all retries exhausted
    raise last_error


def run_agent(user_question):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. You have access to EXACTLY three tools: "
                "calculator, wordcount, document_lookup. No other tools exist. "
                "Never attempt to call any tool other than these three "
                "(for example, never call search, browser, web_search, or brave_search — "
                "these do not exist and calling them will cause an error).\n\n"
                "Decision rule, follow it exactly:\n"
                "1. If the question is about math/arithmetic, call ONLY calculator.\n"
                "2. If the question asks to count words in a given text, call ONLY wordcount.\n"
                "3. If the question is about linear algebra or the textbook content "
                "(e.g. determinants, eigenvalues, matrices, vectors, transformations), "
                "call ONLY document_lookup. Do not answer these from your own knowledge — "
                "you do not have reliable knowledge of this specific textbook's content, "
                "so you must retrieve it rather than guessing or inventing passages.\n"
                "4. For anything else (general knowledge, greetings, opinions), "
                "do NOT call any tool — answer directly in plain text.\n\n"
                "Formatting rule, follow it exactly:\n"
                "- If you call a tool, your entire response must be ONLY the tool call "
                "itself, with no explanatory text, no partial answer, and no commentary "
                "before or after it.\n"
                "- If you are not calling a tool, respond with plain text only, "
                "and do not include any tool call syntax.\n"
                "- Never mix plain text and a tool call in the same response."
            )
        },
        {"role": "user", "content": user_question}
    ]

    # Step 1: send the question + tool definitions to the model
    response = call_with_tool_retry(messages)

    response_message = response.choices[0].message

    # Step 2: check if the model asked for a tool call
    if response_message.tool_calls:

        # add the model's tool-call request to the conversation
        messages.append(response_message)

        for tool_call in response_message.tool_calls:

            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"\n[Tool Call] {function_name}({function_args})")

            # Step 3: actually run the function ourselves
            function_to_call = available_functions[function_name]
            function_result = function_to_call(**function_args)

            print(f"[Tool Result] {function_result}\n")

            # Step 4: send the result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(function_result)
            })

        # Step 4.5: override the earlier "tool call only" formatting rule —
        # for this final call we want a complete, natural-language answer
        messages.append({
            "role": "system",
            "content": (
                "You now have the tool result above. Write the final answer to the "
                "user's original question as a complete, natural-language sentence "
                "that states the actual answer.\n\n"
                "Do NOT reply with just a tool name, a number alone, or any other "
                "bare fragment. Do NOT call any tool in this step. Do NOT add "
                "commentary, speculation, or explanation beyond directly answering "
                "the question.\n\n"
                "Examples of the expected style:\n"
                "- Question: 'whats 47 times 89' -> Answer: '47 times 89 is 4183.'\n"
                "- Question: 'how many words in this sentence \"hello world\"' -> "
                "Answer: 'There are 2 words in that sentence.'\n"
                "- Question: 'what is an eigenvalue' -> Answer: a direct explanation "
                "using only the retrieved passage, in your own words."
            )
        })

        # Step 5: get the model's final answer, now that it has the tool result
        final_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        return final_response.choices[0].message.content

    else:
        # No tool needed, the model answered directly
        return response_message.content


def main():

    # Load the vector store collection so document_lookup works
    load_collection()

    print("Agent ready. Type 'exit' to quit.\n")

    while True:

        question = input("Ask something: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = run_agent(question)

        print("\nFinal Answer:")
        print(answer)
        print()


if __name__ == "__main__":
    main()