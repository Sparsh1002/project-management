from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    JSON,
    Index
)

from app.db.database import Base


class Issue(Base):

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)

    issue_key = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    title = Column(
        String,
        nullable=False,
        index=True
    )

    description = Column(Text)

    """
    Epic / Story / Task / Bug / Sub-task
    """
    type = Column(
        String,
        nullable=False,
        index=True
    )

    status = Column(
        String,
        default="To Do",
        index=True
    )

    priority = Column(
        String,
        default="Medium",
        index=True
    )

    version = Column(
        Integer,
        default=1
    )

    story_points = Column(
        Integer,
        default=0
    )

    labels = Column(
        JSON,
        nullable=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
        index=True
    )

    sprint_id = Column(
        Integer,
        ForeignKey("sprints.id"),
        nullable=True,
        index=True
    )

    assignee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    reporter_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    parent_issue_id = Column(
        Integer,
        ForeignKey("issues.id"),
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


Index("idx_issue_project", Issue.project_id)
Index("idx_issue_sprint", Issue.sprint_id)