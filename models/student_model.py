from sqlalchemy import Column, String, DateTime as SQLDateTime, Date
from config.database import Base
from datetime import datetime

class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    family_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    dob = Column(Date, nullable=False) 
    created_at = Column(SQLDateTime, nullable=False, default=datetime.utcnow)
