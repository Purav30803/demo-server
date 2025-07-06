from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from service.stats_service import get_stats
from loguru import logger
from db.connect_db import get_db

stats_router = APIRouter()

@stats_router.get("/view-stats")
def fetch_stats(db: Session = Depends(get_db)):
    logger.info(f"Fetching stats")
    return get_stats(db)