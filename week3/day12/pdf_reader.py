from pypdf import PdfReader


def read_pdf(file_path):
    """
    Reads a PDF and returns a list of page texts.
    """

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return pages