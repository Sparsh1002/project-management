
from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    issue_id = Column(
        Integer,
        ForeignKey("issues.id")
    )

    parent_comment_id = Column(
        Integer,
        nullable=True
    )

    content = Column(Text)
