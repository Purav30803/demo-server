from pydantic import BaseModel, EmailStr
from datetime import datetime

class CourseCreate(BaseModel):
    id: str = None  # Optional, will be generated if not provided
    courseName: str

    class Config:
        extra = "forbid"  # Forbids extra fields
        error_msg_templates = {
            "value_error.missing": "The field '{loc}' is required but was not provided.",
        }


