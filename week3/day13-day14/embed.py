from pdf_reader import read_pdf
from chunker import split_into_chunks
from vector_store import store_chunks, is_document_indexed


def main():

    pdf_path = "../data/Textbook.pdf"

    if is_document_indexed():
        print("Database already exists.")
        return

    print("Reading PDF...")

    pages = read_pdf(pdf_path)

    print("Creating chunks...")

    all_chunks = []

    for page in pages:
        page_chunks = split_into_chunks(page)
        all_chunks.extend(page_chunks)

    print(f"Total chunks created: {len(all_chunks)}")

    print("Generating embeddings...")

    store_chunks(all_chunks)

    print("Embeddings stored successfully.")


if __name__ == "__main__":
    main()