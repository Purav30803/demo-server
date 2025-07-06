from pydantic import BaseModel, EmailStr
from datetime import datetime

class StudentCreate(BaseModel):
    id: str = None  # Optional, will be generated if not provided
    firstName: str
    familyName: str
    email: EmailStr
    dateOfBirth: datetime

    class Config:
        extra = "forbid"  # Forbids extra fields
        error_msg_templates = {
            "value_error.missing": "The field '{loc}' is required but was not provided.",
            "type_error.email": "The email '{loc}' is not valid. Please provide a correct email.",
        }


