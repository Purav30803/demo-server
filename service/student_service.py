from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.student_model import Student
from schemas.student_schema import StudentCreate
from fastapi.responses import JSONResponse
import random
import string

def create_student(db: Session, student: StudentCreate):

    if not student.firstName or not student.familyName or not student.email or not student.dateOfBirth:
        raise HTTPException(status_code=400, detail="First name, family name, email and date of birth are required")
    # Check if a student with the same email already exists
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # random 10 characters as ID
    def generate_random_id(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    db_student = Student(
        id=generate_random_id(),
        first_name=student.firstName,
        family_name=student.familyName,
        email=student.email,
        dob=student.dateOfBirth
    )

    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating student")

    return JSONResponse(
        status_code=201,
        content={
            "message": "Student created successfully"
        }
    )


def get_students(db: Session, searchTerm: str = None):

    query = db.query(Student)
    if searchTerm:
        searchTerm = searchTerm.strip()
        query = query.filter(
            (Student.first_name.ilike(f"%{searchTerm}%")) |
            (Student.family_name.ilike(f"%{searchTerm}%")) |
            (Student.email.ilike(f"%{searchTerm}%"))
        )
    students = query.all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students


def remove_student(db: Session, student_id: str):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        db.delete(student)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting student")

    return JSONResponse(
        status_code=200,
        content={
            "message": "Student deleted successfully"
        }
    )