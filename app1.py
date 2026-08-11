import streamlit as st
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    extracted_pages = []

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_pages.append(page_text)

    document_text = "\n".join(extracted_pages)

    return document_text, len(pdf_reader.pages)

def split_text_into_chunks(
    text,
    chunk_size=180,
    chunk_overlap=40
):
    words = text.split()
    chunks = []

    step_size = chunk_size - chunk_overlap

    for start_index in range(
        0,
        len(words),
        step_size
    ):
        end_index = start_index + chunk_size

        chunk_words = words[
            start_index:end_index
        ]

        chunk_text = " ".join(chunk_words)

        if chunk_text.strip():
            chunks.append(chunk_text)

    return chunks

def create_chunk_embeddings(
    chunks,
    model
):
    embeddings = model.encode_document(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings

st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="📄",
    layout="wide"
)

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

    document_chunks = split_text_into_chunks(document_text)

    chunk_count = len(document_chunks)

    st.subheader("Ask a question")

    user_question = st.text_input(
    "Enter a question about the document"
    )

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.metric("Pages", page_count)

    with info_col2:
        st.metric("Words", word_count)

    with info_col3:
        st.metric("Chunks", chunk_count)

    with st.expander("Preview extracted text"):
        st.text_area("Document text", document_text, height=300, disabled=True)


    with st.expander("Preview document chunks"):
        preview_count = min(
            3,
            len(document_chunks)
        )

        for index in range(preview_count):
            st.markdown(
                f"**Chunk {index + 1}**"
            )

            st.write(
                document_chunks[index]
            )

            st.divider()
    
