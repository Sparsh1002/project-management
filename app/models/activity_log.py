
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)

    issue_id = Column(Integer)

    action = Column(String)
