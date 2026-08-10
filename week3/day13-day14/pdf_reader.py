import fitz  # pymupdf


def read_pdf(file_path):
    """
    Reads a PDF and returns a list of page texts.
    """

    doc = fitz.open(file_path)

    pages = []

    for page in doc:
        text = page.get_text()

        if text.strip():
            pages.append(text)

    doc.close()

    return pages