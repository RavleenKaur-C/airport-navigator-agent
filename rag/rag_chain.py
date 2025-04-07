import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from rag.retriever import AirportRetriever

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

RAG_TEMPLATE = """
You are a helpful travel assistant. Use the information below to answer the user's question.
If the answer is not found in the context, say "I couldn't find that information."

Context:
{context}

Question:
{question}

Answer as a short, informative paragraph:
"""

rag_prompt = PromptTemplate.from_template(RAG_TEMPLATE)

def run_rag_chain(airport_name: str, user_question: str) -> str:
    retriever = AirportRetriever()

    success = retriever.load_and_index(airport_name)
    if not success:
        return f"Couldn't find Wikivoyage info for {airport_name}."

    chunks = retriever.retrieve_passages(user_question, k=3)
    context = "\n\n".join(chunks)

    full_prompt = rag_prompt.format(context=context, question=user_question)
    answer = llm.invoke(full_prompt).content

    return answer.strip()
