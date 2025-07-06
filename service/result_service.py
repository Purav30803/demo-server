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
    # Check if a result for the same student and course already exists
    existing_result = db.query(Result).filter(
        Result.student_id == result.student_id,
        Result.course_id == result.course_id
    ).first()
    
    if existing_result:
        raise HTTPException(status_code=400, detail="Result already exists for this student and course")
    
    # random 10 characters as ID
    def generate_random_id(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    db_result = Result(
        id=generate_random_id(),
        student_id=result.student_id,
        course_id=result.course_id,
        score=result.score
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

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
    db.delete(result)
    db.commit() 
    return JSONResponse(
        status_code=200,
        content={
            "message": "Result deleted successfully"
        }
    )