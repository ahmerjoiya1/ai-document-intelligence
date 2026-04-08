import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload-pdf/"
ASK_ENDPOINT = f"{BACKEND_URL}/ask"

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

st.subheader("Ask a Question")

query = st.text_input("Ask a question about the uploaded document...")

if st.button("Get Answer"):
    if query.strip():
        try:
            with st.spinner("Generating answer..."):
                response = requests.post(
                    ASK_ENDPOINT,
                    json={"query": query, "top_k": 3},
                    timeout=120
                )

            response.raise_for_status()
            data = response.json()

            st.success("Answer generated")

            st.write("### Answer")
            st.write(data.get("answer", "No answer returned."))

            st.write("### Sources")
            sources = data.get("sources", [])

            if sources:
                for src in sources:
                    st.write(
                        f"- Page {src.get('page', 'N/A')} | {src.get('source', 'Unknown source')}"
                    )
                    st.caption(src.get("preview", ""))
            else:
                st.info("No sources returned.")

        except Exception as e:
            st.error(f"Error getting answer: {e}")
    else:
        st.warning("Please enter a question first.")

