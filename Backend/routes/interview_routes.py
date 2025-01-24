from fastapi import APIRouter

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("/{job_id}")
def start_interview(job_id: int):
    # Simuliere Interviewstart
    return {"message": f"Interview für Job {job_id} gestartet"}
