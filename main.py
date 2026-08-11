import streamlit as st

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