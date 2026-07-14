from pdf_reader import read_pdf
from chunker import split_into_chunks


def main():
    pdf_path = "data/the_museum_curators_last_note.pdf"

    print("Loading PDF...")

    text = read_pdf(pdf_path)

    print("PDF loaded successfully.")
    print()

    chunks = split_into_chunks(text)

    print(f"Number of chunks: {len(chunks)}")
    print()

    for index, chunk in enumerate(chunks[:3], start=1):
        print(f"Chunk {index}")
        print("-" * 50)
        print(chunk)
        print("-" * 50)
        print(f"Characters: {len(chunk)}")
        print(f"Words: {len(chunk.split())}")
        print()


if __name__ == "__main__":
    main()