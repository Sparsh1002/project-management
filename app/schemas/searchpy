from pydantic import BaseModel


class SearchQuery(BaseModel):

    q: str | None = None

    status: str | None = None

    priority: str | None = None

    assignee_id: int | None = None

    limit: int = 20

    offset: int = 0