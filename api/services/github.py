import os

from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import GitHubIssuesLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import utils as chromautils

load_dotenv(find_dotenv(), override=True)


def load_issues(repo=os.environ["GITHUB_REPOSITORY"]):
    loader = GitHubIssuesLoader(
        repo=repo,
        access_token=os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        include_prs=False,
        state="all",
    )

    docs = loader.load()
    docs = chromautils.filter_complex_metadata(docs)
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=30)

    chunks = splitter.split_documents(docs)
    return chunks
