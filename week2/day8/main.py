from .vector_store import store_pdf, search


def main():
    pdf_path = "data/the_museum_curators_last_note.pdf"

    print("Loading PDF and storing chunks...\n")
    store_pdf(pdf_path)

    print("\nVector Store is ready!")
    print("Ask questions about the PDF.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Enter your question: ")

        if query.lower() == "exit":
            print("\nProgram Closed.")
            break

        top_k = int(input("Enter Top K value: "))

        results = search(query, top_k=top_k)

        documents = results["documents"][0]
        distances = results["distances"][0]

        # Check if the best result is relevant
        if distances[0] > 1.5:
            print("\nSorry! I couldn't find relevant information in the PDF.")
            print(f"Closest Distance Score: {distances[0]:.4f}\n")
            continue

        print("\nTop Matching Chunks")
        print("=" * 60)

        for i, (doc, distance) in enumerate(zip(documents, distances), start=1):
            print(f"\nResult {i}")
            print("-" * 50)
            print(doc)
            print(f"\nDistance Score: {distance:.4f}")

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()