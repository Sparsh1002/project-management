
from pydantic import BaseModel

class CreateIssueRequest(BaseModel):
    title: str
    description: str
    type: str
    priority: str
    parent_issue_id: int | None = None

class TransitionIssueRequest(BaseModel):
    new_status: str
    version: int

from pydantic import BaseModel

class UpdateIssueRequest(BaseModel):

    title: str | None = None

    description: str | None = None

    priority: str | None = None

    assignee_id: int | None = None

    sprint_id: int | None = None

    story_points: int | None = None

    labels: list[str] | None = None

    version: int
