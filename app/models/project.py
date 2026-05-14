
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    key = Column(
        String,
        unique=True,
        nullable=False
    )
