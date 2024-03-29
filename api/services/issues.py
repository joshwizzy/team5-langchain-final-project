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
If your response contains an image change the `img` tag attributes to have width="100%" and height="400".
If you don't find the answer in the provided context respond with 'I don't know'
Context: {context}
"""

summarize_system_prompt = """You are an experienced developer familiar with GitHub issues.
Generate a concise summarize a GitHub issue.
Focus on identifying the main problem, potential causes, and any suggested solutions.
Format the response as Markdown.
Here is the GitHub issue:
"""


generate_issue_system_prompt = """You are an experiencedproduct manager at a software development company. 
Generate a Github issue for a feature description that a software engineer can use to implement the feature.
Use markdown format, with subheaders '##'  for each section.
Start your response with a 'Background' section that provide context for current situation, and what would the benefits of the feature be?
Follow up with a 'Problem Statement' section that clearly identifies the issue, its impact, and the need for a solution, e.g.,
"As a `type of user`, I want `some goal` so that `some reason`." →
Follow up with a 'Screenshots' placeholder section with this text
"<! - Provide screenshots or visual aids if applicable →"
Follow up with a 'Acceptance Criteria' section that defines the relevant Acceptence Criteria
Write out the acceptance criteria in Gherkin BDD style from the perspective of the user and preface each AC with a checkbox
Finish with a 'Implementation Notes' section that provides specific technical guidance and considerations for the software engineers who will be implementing this feature.
Here is the feature description:
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


def generate_issue(feature_description: str):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chat_prompt_template = ChatPromptTemplate.from_messages(
        [("system", generate_issue_system_prompt), ("human", "{feature_description}")]
    )
    llm_chain = chat_prompt_template | llm | StrOutputParser()

    from langchain_core.runnables import RunnablePassthrough

    chain = {
        "feature_description": RunnablePassthrough(),
    } | llm_chain

    response = chain.invoke(feature_description)
    return response
