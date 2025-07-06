from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from schemas.student_schema import StudentCreate
from service.student_service import create_student,get_students, remove_student
from loguru import logger
from db.connect_db import get_db

student_router = APIRouter()

@student_router.post("/add-student")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    name = student.firstName + " " + student.familyName
    logger.info(f"Added Student  - {name} with email {student.email}")
    return create_student(db, student)

@student_router.get("/view-students")
def view_students(searchTerm:str,db: Session = Depends(get_db)):
    logger.info("Fetching all students")
    return get_students(db, searchTerm)

@student_router.delete("/delete-student/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    logger.info(f"Deleting student with ID: {student_id}")
    # Implement the delete logic here
    return remove_student(db, student_id)