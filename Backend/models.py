from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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



class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)  # Stelle sicher, dass dieses Feld vorhanden ist
    description = Column(String, nullable=False)
    requirements = Column(String, nullable=True)
    benefits = Column(String, nullable=True)
