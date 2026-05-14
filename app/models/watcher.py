
from sqlalchemy import Column, Integer
from app.db.database import Base

class Watcher(Base):
    __tablename__ = "watchers"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    issue_id = Column(Integer)
