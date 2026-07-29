from langchain_text_splitters import RecursiveCharacterTextSplitter

MIN_CHUNK_LENGTH = 50  # characters — chunks shorter than this are treated as junk


def split_into_chunks(text):
    """
    Splits text into overlapping chunks, filtering out
    near-empty junk chunks (page headers, stray footer lines, etc).
    """

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    # Drop chunks that are too short to carry real content
    filtered_chunks = [
        chunk for chunk in chunks
        if len(chunk.strip()) >= MIN_CHUNK_LENGTH
    ]

    return filtered_chunks