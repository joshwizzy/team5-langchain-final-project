import json
import os

import requests
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


def create_issue(title: str, body: str, labels: list[str] = None):
    url = f"https://api.github.com/repos/%s/issues" % (os.environ["GITHUB_REPOSITORY"])

    headers = {
        "Authorization": "token %s" % os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        "Accept": "application/vnd.github.golden-comet-preview+json",
    }

    payload = {"title": title, "body": body, "labels": labels}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 202:
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
        print("Response:", response.content)
    return response.json()
