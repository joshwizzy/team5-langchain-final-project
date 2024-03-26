from contextlib import asynccontextmanager

from fastapi import FastAPI

from models.issues import IssuesQueryOutput
from data.chroma.issues import create_embeddings
from services.github import load_issues
from services.issues import search

app = FastAPI(
    title="Github Issues PM Assistant",
    description="API Endpoints for a Github Issues PM Assistant",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    issues = load_issues()
    create_embeddings(issues)


@app.get("/healthz")
async def get_status():
    return {"status": "running"}


@app.get("/qa/{query}")
async def query_issues(query: str) -> IssuesQueryOutput:
    return search(query)
