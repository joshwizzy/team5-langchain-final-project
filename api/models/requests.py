from pydantic import BaseModel


class FetchIssuesRequest(BaseModel):
    repo_url: str
