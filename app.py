import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="📄",
    layout="wide"
)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    extracted_pages = []

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_pages.append(page_text)

    document_text = "\n".join(extracted_pages)

    return document_text, len(pdf_reader.pages)



st.title("RAG Docuement Chatbot")

st.write(
    "Upload a PDF document and ask questions "
    "based on its content."
)

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    st.success(f"Uploaded successfully: {uploaded_file.name}")

    document_text, page_count = (
        extract_text_from_pdf(uploaded_file)
    )

    if not document_text.strip():
        st.error(
            "No readable text was found in this PDF. "
            "It may be scanned or image-based."
        )
        st.stop()

    word_count = len(document_text.split())

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.metric("Pages", page_count)

    with info_col2:
        st.metric("Words", word_count)

    with st.expander("Preview extracted text"):
        st.text_area("Document text", document_text, height=300, disabled=True)