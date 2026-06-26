from langchain_ollama import OllamaEmbeddings

def get_embedding():

    return OllamaEmbeddings(
        model="mxbai-embed-large"
    )