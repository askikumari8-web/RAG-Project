import streamlit as st
import os
from ingest import process_pdfs
from rag import ask_question

st.set_page_config(
    page_title="Financial RAG System",
    page_icon="📈",
    layout="centered"
)


os.makedirs("data", exist_ok=True)

# Header Section
st.title("📈 AI Financial Analyst")
st.markdown("Upload your quarterly earnings reports and ask questions to get instant, cited answers.")
st.divider() 


st.subheader("1️⃣ Upload Documents")
uploaded_files = st.file_uploader("Select PDF files to index", type="pdf", accept_multiple_files=True)


if st.button("Index Documents", type="primary"):
    if uploaded_files:
        with st.spinner("Extracting and processing text..."):
            file_paths = []
            for f in uploaded_files:
                file_path = os.path.join("data", f.name)
                with open(file_path, "wb") as buffer:
                    buffer.write(f.getvalue())
                file_paths.append(file_path)
            
            files_processed, chunks_stored = process_pdfs(file_paths)
            st.success(f"✅ Successfully processed {files_processed} files and stored {chunks_stored} text chunks.")
    else:
        st.warning("⚠️ Please upload at least one PDF file first.")

st.divider()


st.subheader("2️⃣ Ask the Assistant")
question = st.text_input(
    "What would you like to know?", 
    placeholder="e.g., What was the total revenue in the last quarter?"
)

if st.button("Submit Question"):
    if question:
        with st.spinner("Searching the documents..."):
            result = ask_question(question, top_k=5)
            
            st.markdown("### Answer")
            st.info(result["answer"])
            
            st.markdown("### 📚 References")
            unique_sources = {f"📄 {s['file']} (Page {s['page']})" for s in result["sources"]}
            for src in unique_sources:
                st.caption(src)
    else:
        st.warning("⚠️ Please enter a question.")