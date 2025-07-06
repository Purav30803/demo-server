from sqlalchemy import Column, String,DateTime
from config.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    course_name = Column(String, nullable=False)