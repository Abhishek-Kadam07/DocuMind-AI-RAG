from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

def ask_question(db, question):

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 20
        }
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an intelligent document assistant.

Answer using ALL relevant information from the context.

If information is present in multiple sections,
combine it into one complete answer.

If the answer is not present, say:
'I could not find this information in the uploaded documents.'

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content, docs