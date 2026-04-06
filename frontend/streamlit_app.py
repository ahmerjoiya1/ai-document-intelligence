import streamlit as st

st.set_page_config(
    page_title="AI Document Intelligence",
    layout="wide"
)

with st.sidebar:
    st.title("📄 AI Doc System")
    st.subheader("Upload PDF")
    st.file_uploader("Choose a PDF", type=["pdf"])

st.title("📄 AI Document Intelligence System")

st.markdown("""
This system allows you to:
- Upload documents
- Ask questions
- Get AI-powered answers
""")

st.chat_input("Ask a question...")