from fastapi import (
    APIRouter,
    HTTPException
)

from app.db.database import SessionLocal

from app.models.sprint import Sprint
from app.models.issue import Issue

from app.schemas.sprint import (
    CreateSprintRequest
)

router = APIRouter(
    prefix="/sprints",
    tags=["Sprints"]
)


@router.post("/")
def create_sprint(
    payload: CreateSprintRequest
):

    db = SessionLocal()

    sprint = Sprint(
        name=payload.name,
        start_date=payload.start_date,
        end_date=payload.end_date,
        project_id=payload.project_id
    )

    db.add(sprint)

    db.commit()

    db.refresh(sprint)

    db.close()

    return sprint


@router.post("/{sprint_id}/start")
def start_sprint(sprint_id: int):

    db = SessionLocal()

    sprint = db.query(Sprint).filter(
        Sprint.id == sprint_id
    ).first()

    if not sprint:

        raise HTTPException(
            status_code=404,
            detail="Sprint not found"
        )

    if sprint.status != "planned":

        raise HTTPException(
            status_code=400,
            detail="Only planned sprints can be started"
        )

    sprint.status = "active"

    db.commit()

    db.refresh(sprint)

    db.close()

    return {
        "message": "Sprint started successfully",
        "sprint": sprint
    }


@router.post("/{sprint_id}/complete")
def complete_sprint(sprint_id: int):

    db = SessionLocal()

    sprint = db.query(Sprint).filter(
        Sprint.id == sprint_id
    ).first()

    if not sprint:

        raise HTTPException(
            status_code=404,
            detail="Sprint not found"
        )

    if sprint.status != "active":

        raise HTTPException(
            status_code=400,
            detail="Only active sprints can be completed"
        )

    issues = db.query(Issue).filter(
        Issue.sprint_id == sprint.id
    ).all()

    completed_story_points = 0

    incomplete_issues = []

    for issue in issues:

        if issue.status == "Done":

            if hasattr(issue, "story_points"):

                completed_story_points += (
                    issue.story_points or 0
                )

        else:

            incomplete_issues.append({
                "issue_id": issue.id,
                "issue_key": issue.issue_key,
                "title": issue.title,
                "status": issue.status
            })

    sprint.status = "completed"

    db.commit()

    db.close()

    return {
        "message": "Sprint completed successfully",

        "velocity": completed_story_points,

        "incomplete_issues": incomplete_issues,

        "carry_over_supported": True
    }

@router.post("/{sprint_id}/issues/{issue_id}")
def move_issue_to_sprint(
    sprint_id: int,
    issue_id: int
):

    db = SessionLocal()

    try:

        sprint = db.query(Sprint).filter(
            Sprint.id == sprint_id
        ).first()

        if not sprint:

            raise HTTPException(
                status_code=404,
                detail="Sprint not found"
            )

        issue = db.query(Issue).filter(
            Issue.id == issue_id
        ).first()

        if not issue:

            raise HTTPException(
                status_code=404,
                detail="Issue not found"
            )

        if issue.project_id != sprint.project_id:

            raise HTTPException(
                status_code=400,
                detail="Sprint and issue belong to different projects"
            )

        issue.sprint_id = sprint.id

        db.commit()

        return {
            "message": "Issue moved to sprint"
        }

    finally:

        db.close()