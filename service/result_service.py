from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.result_schema import ResultCreate
from models.result_model import Result
from fastapi.responses import JSONResponse
import random
import string
from models.course_model import Course
from models.student_model import Student
from sqlalchemy import or_

def create_result(db: Session, result: ResultCreate):
    
    if not result.student_id or not result.course_id or result.score is None:
        raise HTTPException(status_code=400, detail="Student ID, Course ID and Score are required")

    existing_result = db.query(Result).filter(
        Result.student_id == result.student_id,
        Result.course_id == result.course_id
    ).first()
    
    if existing_result:
        raise HTTPException(status_code=400, detail="Result already exists for this student and course")
    
    # random 10 characters as ID
    def generate_random_id(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    # check if student exists
    student = db.query(Student).filter(Student.id == result.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    course = db.query(Course).filter(Course.id == result.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_result = Result(
        id=generate_random_id(),
        student_id=result.student_id,
        course_id=result.course_id,
        score=result.score
    )

    try:
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating result")

    return JSONResponse(
        status_code=201,
        content={
            "message": "Result created successfully"
        }
    )

def get_results(db: Session, searchTerm: str = None):
    query = db.query(Result).join(Result.course).join(Result.student)

    if searchTerm:
        searchTerm = f"%{searchTerm.lower()}%"
        query = query.filter(
            or_(
                Course.course_name.ilike(searchTerm),
                (Student.first_name + ' ' + Student.family_name).ilike(searchTerm)
            )
        )

    results = query.all()

    result_list = []
    for result in results:
        result_list.append({
            "id": result.id,
            "course_name": result.course.course_name,
            "student_name": f"{result.student.first_name} {result.student.family_name}",
            "score": result.score,
        })

    return result_list

def remove_result(db: Session, result_id: str):
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    try:
        db.delete(result)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting result")

    return JSONResponse(
        status_code=200,
        content={
            "message": "Result deleted successfully"
        }
    )