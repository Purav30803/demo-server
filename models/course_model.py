from sqlalchemy import Column, String, DateTime as SQLDateTime
from config.database import Base
from datetime import datetime

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    created_at = Column(SQLDateTime, nullable=False, default=datetime.utcnow)