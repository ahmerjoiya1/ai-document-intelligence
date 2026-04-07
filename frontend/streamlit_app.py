import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload-pdf"

st.set_page_config(
    page_title="AI Document Intelligence",
    layout="wide"
)

with st.sidebar:
    st.title("📄 AI Doc System")
    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Upload"):
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
            }

            try:
                with st.spinner("Uploading..."):
                    response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=120)

                response.raise_for_status()
                st.success("Upload successful")
                st.json(response.json())

            except Exception as e:
                st.error(f"Upload failed: {e}")

st.title("📄 AI Document Intelligence System")

st.markdown("""
This system allows you to:
- Upload documents
- Ask questions
- Get AI-powered answers
""")

st.chat_input("Ask a question...")