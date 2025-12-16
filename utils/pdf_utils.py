# from pypdf import PdfReader

# def extract_text_from_pdf(pdf_file):
#     reader = PdfReader(pdf_file)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() + "\n"
#     return text

from pypdf import PdfReader

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    pages_data = []

    for page_no, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_data.append({
                "text": text,
                "page": page_no + 1,
                "source": pdf_file.name
            })
    return pages_data
