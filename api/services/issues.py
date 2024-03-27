from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
)

from data.chroma import issues
from models.issues import IssuesQueryOutput

system_prompt = """
You are a project manager assistant. Your job is to help answer questions about a github project's issues.
The context is a combination of all github issues filtered by use of a vector database.
Use the following pieces of context to answer the user's question.
If you don't find the answer in the provided context respond with 'I don't know'
Context: {context}
"""


def search(query: str):
    docs = issues.similarity_search(query)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chat_prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{question}")]
    )
    llm_chain = chat_prompt_template | llm | StrOutputParser()

    from langchain_core.runnables import RunnablePassthrough

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    content = format_docs(docs)

    rag_chain = {
        "context": lambda x: content,
        "question": RunnablePassthrough(),
    } | llm_chain

    response = rag_chain.invoke(query)
    return IssuesQueryOutput(query=query, response=response)
