import os

from contextlib import asynccontextmanager

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

from models.issues import (
    IssuesQueryOutput,
    SummarizeIssueOutput,
    SummarizeIssueRequest,
    CreateIssueRequest,
    CreateIssueOutput,
)
from models.requests import FetchIssuesRequest
from data.chroma.issues import create_embeddings
from services.github import add_issue, fetch_issue, load_issues
from services.issues import generate_issue, search, summarize


@asynccontextmanager
async def lifespan(app: FastAPI):
    issues = load_issues()
    create_embeddings(issues)
    yield


load_dotenv(find_dotenv(), override=True)


X_API_KEY = APIKeyHeader(name="X-API-Key", auto_error=False)


def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    api_key = os.environ.get("API_KEY", None)

    if api_key is None:
        return

    if x_api_key != api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key. Check that you are passing a 'X-API-Key' on your header.",
        )


app = FastAPI(
    title="Github Issues PM Assistant",
    description="API Endpoints for a Github Issues PM Assistant",
    lifespan=lifespan,
)


@app.get("/healthz")
async def get_status():
    return {"status": "running"}


@app.get("/qa/{query}", dependencies=[Depends(api_key_auth)])
async def query_issues(query: str) -> IssuesQueryOutput:
    return search(query)


@app.post("/fetch-issues", dependencies=[Depends(api_key_auth)])
async def fetch_issues(request: FetchIssuesRequest):
    repo = request.repo_url

    issues = load_issues(repo)

    create_embeddings(issues)

    return {"status": "done"}


@app.post("/summarize", dependencies=[Depends(api_key_auth)])
async def summarize_issue(request: SummarizeIssueRequest) -> SummarizeIssueOutput:
    issue = fetch_issue(request.issue_path)
    return summarize(issue)


@app.post("/generate-issue", dependencies=[Depends(api_key_auth)])
async def create_issue(request: CreateIssueRequest) -> CreateIssueOutput:
    llm_response = generate_issue(request.feature_description)
    url = html_url = None
    if request.create_issue:
        issue = add_issue(request.issue_title, llm_response, repo=request.repo_url)
        url = issue["url"]
        html_url = issue["html_url"]
    return CreateIssueOutput(response=llm_response, url=url, html_url=html_url)
