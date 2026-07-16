from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_into_chunks(text):
    """
    Splits text into overlapping chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_text(text)