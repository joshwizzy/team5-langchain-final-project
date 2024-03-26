from pydantic import BaseModel


class IssuesQueryOutput(BaseModel):
    query: str
    response: str
