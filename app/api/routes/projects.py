
from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal
from app.models.activity_log import ActivityLog
from app.models.issue import Issue
from app.models.project import Project
from app.models.sprint import Sprint
from app.schemas.project import CreateProjectRequest

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post("/")
def create_project(payload: CreateProjectRequest):

    db = SessionLocal()

    project = Project(
        name=payload.name,
        key=payload.key
    )

    db.add(project)
    db.commit()

    return project

@router.get("/")
def list_projects():
    db = SessionLocal()

    return db.query(Project).all()

@router.get("/{project_id}/sprints")
def list_project_sprints(project_id: int):

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

        sprints = db.query(Sprint).filter(
            Sprint.project_id == project_id
        ).all()

        return sprints

    finally:

        db.close()

@router.get("/{project_id}/activity")
def get_project_activity(
    project_id: int,
    limit: int = 20,
    offset: int = 0
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


        issue_ids = db.query(Issue.id).filter(
            Issue.project_id == project_id
        ).all()

        issue_ids = [
            issue_id[0]
            for issue_id in issue_ids
        ]

        activities = db.query(ActivityLog).filter(
            ActivityLog.issue_id.in_(issue_ids)
        ).offset(offset).limit(limit).all()

        return activities

    finally:

        db.close()

@router.get("/{project_id}/board")
def get_board_state(project_id: int):

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

        issues = db.query(Issue).filter(
            Issue.project_id == project_id
        ).all()

        board = {
            "To Do": [],
            "In Progress": [],
            "In Review": [],
            "Done": []
        }

        for issue in issues:

            board.setdefault(
                issue.status,
                []
            ).append({
                "id": issue.id,
                "issue_key": issue.issue_key,
                "title": issue.title,
                "priority": issue.priority,
                "type": issue.type
            })

        return board

    finally:

        db.close()
