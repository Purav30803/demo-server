from sqlalchemy import Column, String, DateTime as SQLDateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    score = Column(String, nullable=False)
    created_at = Column(SQLDateTime, nullable=False, default=datetime.utcnow)

    # relationships
    course = relationship("Course", passive_deletes=True)
    student = relationship("Student", passive_deletes=True)

    def __repr__(self):
        return f"<Result(id={self.id}, student_id={self.student_id}, course_id={self.course_id}, score={self.score})>"
