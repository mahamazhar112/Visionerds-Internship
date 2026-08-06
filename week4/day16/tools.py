from vector_store import retrieve_chunks, load_collection


def calculator(a, b, operation):
    if operation == '+':
        return a+b
    elif operation == '-':
        return a-b
    elif operation == "/":
        if(b==0):
          return ("Error, cannot divide by zero")
        else:
          return a/b
    elif operation == '*':
        return a*b


def wordcount(text):
    words = text.split()
    return len(words)


def document_lookup(query):
    results = retrieve_chunks(query, top_k=8)
    docs = results["documents"][0]
    distances = results["distances"][0]

    print(f"[Retrieval distances] {distances}")

    # sort by distance and just take the single best match
    paired = sorted(zip(docs, distances), key=lambda x: x[1])
    best_doc, best_dist = paired[0]

    return best_doc


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Performs basic math operations: add, subtract, multiply, divide",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "first number"},
                    "b": {"type": "number", "description": "second number"},
                    "operation": {"type": "string", "enum": ["+", "-", "*", "/"]}
                },
                "required": ["a", "b", "operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wordcount",
            "description": "counts words in a sentence",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "the text to count words in"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "document_lookup",
            "description": "Searches the linear algebra textbook and returns relevant passages for a given query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "the question or topic to search for in the document"}
                },
                "required": ["query"]
            }
        }
    }
]