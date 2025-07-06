from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from schemas.course_schema import CourseCreate
from service.course_service import create_course, get_courses , remove_course
from loguru import logger
from db.connect_db import get_db

course_router = APIRouter()

@course_router.post("/add-course")
def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    logger.info(f"Added Course  - {course.courseName}")
    return create_course(db, course)

@course_router.get("/view-courses")
def view_courses(searchTerm:str,db: Session = Depends(get_db)):
    logger.info("Fetching all courses")
    return get_courses(db, searchTerm)

@course_router.delete("/delete-course/{course_id}")
def delete_course(course_id: str, db: Session = Depends(get_db)):
    logger.info(f"Deleting course with ID: {course_id}")
    return remove_course(db, course_id)