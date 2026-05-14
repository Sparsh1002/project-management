from fastapi import APIRouter, Depends

from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import or_

from app.db.database import SessionLocal

from app.models.issue import Issue
from app.models.comment import Comment
from app.utils.security import security

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def search_issues(
    q: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    db = SessionLocal()

    try:

        query = (
            db.query(Issue)
            .outerjoin(
                Comment,
                Issue.id == Comment.issue_id
            )
        )

        if q:

            query = query.filter(

                or_(

                    Issue.title.ilike(
                        f"%{q}%"
                    ),

                    Issue.description.ilike(
                        f"%{q}%"
                    ),

                    Comment.content.ilike(
                        f"%{q}%"
                    )
                )
            )

        if status:

            query = query.filter(
                Issue.status == status
            )

        if priority:

            query = query.filter(
                Issue.priority == priority
            )

        if assignee_id:

            query = query.filter(
                Issue.assignee_id == assignee_id
            )


        issues = (
            query
            .distinct()
            .offset(offset)
            .limit(limit)
            .all()
        )

        return issues

    finally:

        db.close()