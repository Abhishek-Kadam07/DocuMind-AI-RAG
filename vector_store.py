from langchain_chroma import Chroma

def create_vector_db(chunks, embedding):

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="chroma_db"
    )

    return db