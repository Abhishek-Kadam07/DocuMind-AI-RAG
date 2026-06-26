from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader
)

def load_document(file_path):

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)

    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)

    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)

    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)

    else:
        return []

    return loader.load()