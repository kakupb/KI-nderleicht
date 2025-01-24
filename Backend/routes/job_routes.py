from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy.orm import Session
from models import JobPosting
from schemas import JobCreate, JobResponse  # Importiere die richtigen Klassen
from database import get_db
from routes.auth_routes import verify_admin

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Erstelle eine neue Stellenanzeige
@router.post("/")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = JobPosting(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# Hole alle Stellenanzeigen
@router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(JobPosting).all()

# Hole eine Stellenanzeige anhand der ID
@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Stellenanzeige nicht gefunden")
    return job

# Lösche eine Stellenanzeige
@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), admin: bool = Depends(verify_admin)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Stellenanzeige nicht gefunden")
    db.delete(job)
    db.commit()
    return {"message": "Stellenanzeige erfolgreich gelöscht"}