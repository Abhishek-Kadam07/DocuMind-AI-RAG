import streamlit as st
import os

from document_loader import load_document
from chunking import create_chunks
from embeddings import get_embedding
from vector_store import create_vector_db
from rag_pipeline import ask_question

# Create folders automatically
os.makedirs("uploads", exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "db" not in st.session_state:
    st.session_state.db = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "all_docs" not in st.session_state:
    st.session_state.all_docs = []

if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []

st.title("📚 DocuMind AI")
st.write("Upload documents and ask questions about them.")

# ---------------- FILE UPLOAD ----------------
uploaded_files = st.file_uploader(
    "Upload Documents",
    accept_multiple_files=True,
    type=["pdf", "docx", "txt", "csv"]
)

if uploaded_files:

    new_files = []

    for file in uploaded_files:
        if file.name not in st.session_state.uploaded_file_names:
            new_files.append(file)

    if new_files:

        with st.spinner("Processing documents..."):

            for file in new_files:

                path = os.path.join(
                    "uploads",
                    file.name
                )

                with open(path, "wb") as f:
                    f.write(file.getbuffer())

                docs = load_document(path)

                for doc in docs:
                    doc.metadata["source_file"] = file.name

                st.session_state.all_docs.extend(docs)
                st.session_state.uploaded_file_names.append(
                    file.name
                )

            chunks = create_chunks(
                st.session_state.all_docs
            )

            embedding = get_embedding()

            st.session_state.db = create_vector_db(
                chunks,
                embedding
            )

        st.success(
            f"✅ Total Documents Loaded: {len(st.session_state.uploaded_file_names)}"
        )

# ---------------- SIDEBAR ----------------
if st.session_state.uploaded_file_names:

    st.sidebar.header("📄 Uploaded Documents")

    for file_name in st.session_state.uploaded_file_names:
        st.sidebar.write(f"✅ {file_name}")

# ---------------- ASK QUESTIONS ----------------
if st.session_state.db is not None:

    question = st.chat_input(
        "Ask a question about your documents..."
    )

    if question:

        with st.spinner("Generating Answer..."):

            answer, sources = ask_question(
                st.session_state.db,
                question
            )

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

# ---------------- DISPLAY CHAT ----------------
if st.session_state.chat_history:

    st.subheader("💬 Chat History")

    for chat in reversed(
        st.session_state.chat_history
    ):

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

# ---------------- BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

with col2:
    if st.button("🆕 Reset All Documents"):
        st.session_state.db = None
        st.session_state.chat_history = []
        st.session_state.all_docs = []
        st.session_state.uploaded_file_names = []
        st.rerun()