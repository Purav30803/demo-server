from pydantic import BaseModel, EmailStr
from datetime import datetime

class ResultCreate(BaseModel):
    id: str = None  # Optional, will be generated if not provided
    student_id: str
    course_id: str
    score: str


    class Config:
        extra = "forbid"  # Forbids extra fields
        error_msg_templates = {
            "value_error.missing": "The field '{loc}' is required but was not provided.",
        }
