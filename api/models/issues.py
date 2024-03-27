from pydantic import BaseModel


class IssuesQueryOutput(BaseModel):
    query: str
    response: str


class SummarizeIssueRequest(BaseModel):
    issue_path: str


class SummarizeIssueOutput(BaseModel):
    response: str
