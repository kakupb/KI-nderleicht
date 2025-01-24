from pydantic import BaseModel
from typing import Optional

class JobBase(BaseModel):
    title: str
    company: str
    description: str
    requirements: Optional[str] = None
    benefits: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int

    class Config:
        orm_mode = True  # Ermöglicht die Konvertierung von SQLAlchemy-Modellen in Pydantic