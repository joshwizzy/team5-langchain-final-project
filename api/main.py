from contextlib import asynccontextmanager

from fastapi import FastAPI

from models.issues import IssuesQueryOutput
from models.requests import FetchIssuesRequest
from data.chroma.issues import create_embeddings
from services.github import load_issues
from services.issues import search


@asynccontextmanager
async def lifespan(app: FastAPI):
    issues = load_issues()
    create_embeddings(issues)
    yield


app = FastAPI(
    title="Github Issues PM Assistant",
    description="API Endpoints for a Github Issues PM Assistant",
    lifespan=lifespan,
)


@app.get("/healthz")
async def get_status():
    return {"status": "running"}


@app.get("/qa/{query}")
async def query_issues(query: str) -> IssuesQueryOutput:
    return search(query)


@app.post("/fetch-issues")
async def fetch_issues(request: FetchIssuesRequest):
    repo = request.repo_url

    issues = load_issues(repo)

    create_embeddings(issues)

    return {'status': 'done'}
