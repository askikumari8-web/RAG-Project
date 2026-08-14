from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def ask_question(question, top_k=5):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    docs = retriever.invoke(question)
    
    context_parts = []
    for d in docs:
        file_name = d.metadata.get('source', 'Unknown').split('/')[-1]
        page_num = d.metadata.get('page', 'Unknown')
        context_parts.append(f"Document: {file_name} Page: {page_num}\nContent: {d.page_content}")
    
    context = "\n\n".join(context_parts)

    system_prompt = "Answer only from the context provided below. If the context does not contain the answer, reply that the information is not available in the uploaded documents."

    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    
    messages = [
        {"role": "system", "content": system_prompt + "\n\nContext:\n" + context},
        {"role": "user", "content": question}
    ]
    
    response = llm.invoke(messages)
    
    sources = [{"file": d.metadata.get("source").split('/')[-1], "page": d.metadata.get("page")} for d in docs]
    
    return {"answer": response.content, "sources": sources}