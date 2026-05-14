
from pydantic import BaseModel

class AddCommentRequest(BaseModel):
    content: str
    parent_comment_id: int | None = None
