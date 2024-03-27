from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
)

from data.chroma import issues
from models.issues import IssuesQueryOutput, SummarizeIssueOutput

system_prompt = """
You are a project manager assistant. Your job is to help answer questions about a github project's issues.
The context is a combination of all github issues filtered by use of a vector database.
Use the following pieces of context to answer the user's question.
If you don't find the answer in the provided context respond with 'I don't know'
Context: {context}
"""

summarize_system_prompt = """You are an experienced developer familiar with GitHub issues.
Generate a concise summarize a GitHub issue.
Focus on identifying the main problem, potential causes, and any suggested solutions.
Format the response as Markdown.
Here is the GitHub issue:
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


def format_issue(issue: dict) -> str:
    fields = {
        "Title": issue["title"],
        "Body": issue["body"],
        "Date Submited": issue["created_at"],
        "State": issue["state"],
        "Submitted by": issue["user"]["login"],
    }
    issue_text = ""
    for title, value in fields.items():
        issue_text += f"{title}: {value}\n\n"
    return issue_text


def summarize(issue: dict):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chat_prompt_template = ChatPromptTemplate.from_messages(
        [("system", summarize_system_prompt), ("human", "{issue}")]
    )
    llm_chain = chat_prompt_template | llm | StrOutputParser()

    from langchain_core.runnables import RunnablePassthrough

    issue = format_issue(issue)
    chain = {
        "context": lambda x: issue,
        "issue": RunnablePassthrough(),
    } | llm_chain

    response = chain.invoke(issue)
    return SummarizeIssueOutput(response=response)
