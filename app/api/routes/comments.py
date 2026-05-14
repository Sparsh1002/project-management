from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from fastapi.security import HTTPAuthorizationCredentials

from app.db.database import SessionLocal

from app.models.issue import Issue
from app.models.comment import Comment
from app.models.activity_log import ActivityLog

from app.schemas.comment import (
    AddCommentRequest
)
from app.utils.security import security
from app.utils.mentions import create_mention_notifications

router = APIRouter(
    prefix="/issues",
    tags=["Comments"]
)


@router.get("/{issue_id}/comments")
def list_issue_comments(issue_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):

    db = SessionLocal()

    try:

        issue = db.query(Issue).filter(
            Issue.id == issue_id
        ).first()

        if not issue:

            raise HTTPException(
                status_code=404,
                detail="Issue not found"
            )

        comments = db.query(Comment).filter(
            Comment.issue_id == issue_id
        ).all()

        return comments

    finally:

        db.close()


@router.post("/{issue_id}/comments")
def add_comment(
    issue_id: int,
    payload: AddCommentRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    db = SessionLocal()

    try:

        issue = db.query(Issue).filter(
            Issue.id == issue_id
        ).first()

        if not issue:

            raise HTTPException(
                status_code=404,
                detail="Issue not found"
            )

        if payload.parent_comment_id:

            parent_comment = db.query(Comment).filter(
                Comment.id == payload.parent_comment_id
            ).first()

            if not parent_comment:

                raise HTTPException(
                    status_code=404,
                    detail="Parent comment not found"
                )

        comment = Comment(
            issue_id=issue_id,

            content=payload.content,

            parent_comment_id=payload.parent_comment_id
        )

        db.add(comment)

        db.flush()
        

        activity_log = ActivityLog(
            issue_id=issue.id,
            action="Comment added"
        )

        db.add(activity_log)

        create_mention_notifications(
            db=db,
            content=payload.content
        )

        db.commit()

        db.refresh(comment)

        return comment

    finally:

        db.close()