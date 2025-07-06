from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.course_model import Course
from schemas.course_schema import CourseCreate
from fastapi.responses import JSONResponse
import random
import string

def create_course(db: Session, course: CourseCreate):

    if not course.courseName:
        raise HTTPException(status_code=400, detail="Course name is required")

    existing_course = db.query(Course).filter(Course.course_name == course.courseName).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course already exists")

    def generate_random_id(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    db_course = Course(
        id=generate_random_id(),
        course_name=course.courseName
    )

    try:
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating course")

    return JSONResponse(
        status_code=201,
        content={
            "message": "Course created successfully"
        }
    )


def get_courses(db: Session, searchTerm: str = None):

    query = db.query(Course)
    if searchTerm:
        searchTerm = searchTerm.strip()
        query = query.filter(
            (Course.course_name.ilike(f"%{searchTerm}%"))
        )
    courses = query.all()
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses

    
def remove_course(db: Session, course_id: str):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    try:
        db.delete(course)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting course")
    return JSONResponse(
        status_code=200,
        content={
            "message": "Course deleted successfully"
        }
    )