from typing import Optional

from pydantic import BaseModel


class IssuesQueryOutput(BaseModel):
    query: str
    response: str


class SummarizeIssueRequest(BaseModel):
    issue_path: str


class SummarizeIssueOutput(BaseModel):
    response: str


class CreateIssueRequest(BaseModel):
    feature_description: str
    create_issue: Optional[bool] = False
    issue_title: Optional[str] = None
    repo_url: Optional[str] = None


class CreateIssueOutput(BaseModel):
    response: str
    url: Optional[str] = None
    html_url: Optional[str] = None
