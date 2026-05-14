from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date
)

from app.db.database import Base


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    status = Column(
        String,
        default="planned"
    )

    start_date = Column(Date)

    end_date = Column(Date)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )