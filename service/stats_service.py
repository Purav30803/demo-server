from sqlalchemy.orm import Session
from models.result_model import Result
from fastapi.responses import JSONResponse
from models.course_model import Course
from models.student_model import Student

def get_stats(db: Session):
    total_students = db.query(Student).count()
    total_courses = db.query(Course).count()
    total_results = db.query(Result).count()
    
    return JSONResponse(
        status_code=200,
        content={
            "total_students": total_students,
            "total_courses": total_courses,
            "total_results": total_results
        }
    )