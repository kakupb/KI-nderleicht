from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from pathlib import Path

router = APIRouter(prefix="/uploads", tags=["Uploads"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/cv/{job_id}")
async def upload_cv(job_id: int, file: UploadFile = File(...)):
    save_path = Path(UPLOAD_DIR) / f"job_{job_id}" / "cv"
    save_path.mkdir(parents=True, exist_ok=True)
    file_path = save_path / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "CV erfolgreich hochgeladen", "file_path": str(file_path)}

@router.post("/letter/{job_id}")
async def upload_letter(job_id: int, file: UploadFile = File(...)):
    save_path = Path(UPLOAD_DIR) / f"job_{job_id}" / "letters"
    save_path.mkdir(parents=True, exist_ok=True)
    file_path = save_path / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "Anschreiben erfolgreich hochgeladen", "file_path": str(file_path)}
