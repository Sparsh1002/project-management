
import asyncio
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from fastapi.security import HTTPAuthorizationCredentials

from app.db.database import SessionLocal

from app.models.project import Project
from app.models.issue import Issue
from app.models.activity_log import ActivityLog

from app.schemas.issue import (
    CreateIssueRequest,
    UpdateIssueRequest,
    TransitionIssueRequest
)
from app.utils.security import security
from app.websocket.manager import (
    broadcast_event
)

router = APIRouter(
    prefix="/issues",
    tags=["Issues"]
)


VALID_TRANSITIONS = {
    "To Do": ["In Progress"],
    "In Progress": ["In Review"],
    "In Review": ["Done"]
}


@router.post("/{project_id}")
def create_issue(
    project_id: int,
    payload: CreateIssueRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    db = SessionLocal()

    try:

        project = db.query(Project).filter(
            Project.id == project_id
        ).first()

        if not project:

            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        if payload.parent_issue_id:

            parent_issue = db.query(Issue).filter(
                Issue.id == payload.parent_issue_id
            ).first()

            if not parent_issue:

                raise HTTPException(
                    status_code=404,
                    detail="Parent issue not found"
                )
            
        total_issues = db.query(Issue).filter(
            Issue.project_id == project_id
        ).count()

        issue_key = (
            f"{project.key}-{total_issues + 1}"
        )

        current_user = request.state.user

        issue = Issue(
            issue_key=issue_key,

            title=payload.title,

            description=payload.description,

            type=payload.type,

            priority=payload.priority,

            project_id=project_id,

            parent_issue_id=payload.parent_issue_id,

            reporter_id=current_user.id
        )

        db.add(issue)

        db.flush()

        activity_log = ActivityLog(
            issue_id=issue.id,
            action="Issue created"
        )

        db.add(activity_log)

        db.commit()

        db.refresh(issue)

        asyncio.create_task(
            broadcast_event(
                "issue_created",
                {
                    "issue_id": issue.id,
                    "title": issue.title
                }
            )
        )

        return issue

    finally:

        db.close()


@router.patch("/{issue_id}")
def update_issue(
    issue_id: int,
    payload: UpdateIssueRequest,
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

        if issue.version != payload.version:

            raise HTTPException(
                status_code=409,
                detail="Issue was modified by another user"
            )
        
        if payload.title is not None:
            issue.title = payload.title

        if payload.description is not None:
            issue.description = payload.description

        if payload.priority is not None:
            issue.priority = payload.priority

        if payload.assignee_id is not None:
            issue.assignee_id = payload.assignee_id

        if payload.story_points is not None:
            issue.story_points = payload.story_points

        if payload.labels is not None:
            issue.labels = payload.labels

        issue.version += 1

        activity_log = ActivityLog(
            issue_id=issue.id,
            action="Issue updated"
        )

        db.add(activity_log)

        db.commit()

        asyncio.create_task(
            broadcast_event(
                "issue_updated",
                {
                    "issue_id": issue.id,
                    "title": issue.title
                }
            )
        )

        db.refresh(issue)

        return issue

    finally:

        db.close()


@router.post("/{issue_id}/transitions")
def transition_issue(
    issue_id: int,
    payload: TransitionIssueRequest,
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


        allowed = VALID_TRANSITIONS.get(
            issue.status,
            []
        )

        if payload.new_status not in allowed:

            raise HTTPException(
                status_code=422,
                detail=f"Allowed transitions: {allowed}"
            )

        if (
            payload.new_status == "In Review"
            and not issue.assignee_id
        ):

            raise HTTPException(
                status_code=422,
                detail="Assignee required before review"
            )
        
        if issue.version != payload.version:

            raise HTTPException(
                status_code=409,
                detail="Issue modified by another user"
            )

        old_status = issue.status
        issue.status = payload.new_status

        issue.version += 1

        activity_log = ActivityLog(
            issue_id=issue.id,
            action=f"{old_status} -> {payload.new_status}"
        )

        db.add(activity_log)

        db.commit()

        db.refresh(issue)

        asyncio.create_task(
            broadcast_event(
                "issue_transitioned",
                {
                    "issue_id": issue.id,
                    "status": issue.status
                }
            )
        )

        return {
            "message": "Issue transitioned successfully",
            "issue": issue
        }

    finally:

        db.close()