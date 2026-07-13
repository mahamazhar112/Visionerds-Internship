from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample sentences
sentences = [
    "I love cats.",
    "Cats are wonderful pets.",
    "Python is a great programming language.",
    "I enjoy writing Python code.",
    "Pizza is my favorite food.",
    "The weather is sunny today."
]

# Generate embeddings
embeddings = model.encode(sentences)

print("=" * 70)
print("Sentence Embeddings Generated Successfully!")
print("=" * 70)

# Print Cosine Similarity Matrix
print("\nCosine Similarity Matrix:\n")

print("      ", end="")
for i in range(len(sentences)):
    print(f"S{i+1:^8}", end="")
print()

for i in range(len(sentences)):
    print(f"S{i+1} ", end="")
    for j in range(len(sentences)):
        similarity = cos_sim(embeddings[i], embeddings[j]).item()
        print(f"{similarity:^8.2f}", end="")
    print()

# Print sentence key
print("\nSentence Key:")
for i, sentence in enumerate(sentences):
    print(f"S{i+1}: {sentence}")

# Similarity threshold
THRESHOLD = 0.60


# Function to find the most similar sentence
def most_similar(query):
    query_embedding = model.encode(query)

    best_score = -1
    best_sentence = ""

    for sentence, embedding in zip(sentences, embeddings):
        score = cos_sim(query_embedding, embedding).item()

        if score > best_score:
            best_score = score
            best_sentence = sentence

    if best_score >= THRESHOLD:
        return best_sentence, best_score
    else:
        return None, best_score


print("\n" + "=" * 70)
print("Semantic Sentence Search")
print("Type 'exit' to quit.")
print("=" * 70)

# User input loop
while True:
    query = input("\nEnter a sentence: ")

    if query.lower() == "exit":
        print("\nProgram Closed.")
        break

    sentence, score = most_similar(query)

    if sentence is not None:
        print("\nMost Similar Sentence:")
        print(sentence)
        print(f"Similarity Score: {score:.2f}")
    else:
        print("\nNo similar sentence found.")
        print(f"Highest Similarity Score: {score:.2f}")