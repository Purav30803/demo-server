from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from schemas.result_schema import ResultCreate
from service.result_service import create_result, get_results, remove_result
from loguru import logger
from db.connect_db import get_db

result_router = APIRouter()

@result_router.post("/add-result")
def add_result(result: ResultCreate, db: Session = Depends(get_db)):
    logger.info(f"Added Result  - {result.student_id} for course {result.course_id} with score {result.score}")
    return create_result(db, result)

@result_router.get("/view-results")
def view_results(searchTerm:str,db: Session = Depends(get_db)):
    logger.info("Fetching all results")
    return get_results(db, searchTerm)

@result_router.delete("/delete-result/{result_id}")
def delete_result(result_id: str, db: Session = Depends(get_db)):
    logger.info(f"Deleting result with ID: {result_id}")
    return remove_result(db, result_id)