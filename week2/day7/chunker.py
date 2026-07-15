from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_into_chunks(text):
    """ Splits text into overlapping chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
         separators=[" ", ""],
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    return chunks