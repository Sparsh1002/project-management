from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from fastapi.security import HTTPAuthorizationCredentials

from app.db.database import SessionLocal

from app.models.issue import Issue
from app.models.watcher import Watcher
from app.utils.security import security

router = APIRouter(
    prefix="/issues",
    tags=["Watchers"]
)


@router.post("/{issue_id}/watch")
def watch_issue(
    issue_id: int,
    request: Request,
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

        current_user = request.state.user

        existing = db.query(Watcher).filter(
            Watcher.issue_id == issue_id,
            Watcher.user_id == current_user.id
        ).first()

        if existing:

            return {
                "message": "Already watching"
            }

        watcher = Watcher(
            issue_id=issue_id,
            user_id=current_user.id
        )

        db.add(watcher)

        db.commit()

        return {
            "message": "Watching issue"
        }

    finally:

        db.close()


@router.delete("/{issue_id}/watch")
def unwatch_issue(
    issue_id: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    db = SessionLocal()

    try:

        current_user = request.state.user

        watcher = db.query(Watcher).filter(
            Watcher.issue_id == issue_id,
            Watcher.user_id == current_user.id
        ).first()

        if not watcher:

            raise HTTPException(
                status_code=404,
                detail="Watcher not found"
            )

        db.delete(watcher)

        db.commit()

        return {
            "message": "Stopped watching issue"
        }

    finally:

        db.close()