from sqlalchemy import Column, String,DateTime
from config.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    family_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    dob = Column(DateTime, nullable=False)