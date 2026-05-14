from datetime import date

from pydantic import BaseModel


class CreateSprintRequest(BaseModel):

    name: str

    start_date: date

    end_date: date

    project_id: int