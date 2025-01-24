from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from pathlib import Path
import shutil
from pdfminer.high_level import extract_text
from docx import Document
from fastapi import FastAPI
from routes import auth_routes, job_routes, upload_routes, interview_routes
from database import engine, Base, init_db

# Initialisiere die Datenbank
init_db()

# Initialisiere Datenbank
Base.metadata.create_all(bind=engine)

# Initialisiere FastAPI
app = FastAPI()

# Routen registrieren
app.include_router(job_routes.router)
app.include_router(upload_routes.router)
app.include_router(interview_routes.router)
app.include_router(auth_routes.router)


# CORS konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend-URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basisverzeichnisse für hochgeladene Dateien
CV_DIR = {"original": "uploaded_files/cv/original", "text": "uploaded_files/cv/text"}
LETTER_DIR = {"original": "uploaded_files/letter/original", "text": "uploaded_files/letter/text"}

# Verzeichnisse erstellen
for path in [*CV_DIR.values(), *LETTER_DIR.values()]:
    os.makedirs(path, exist_ok=True)

# Unterstützte Dateiformate
SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

# Hilfsfunktion: Text aus Dateien extrahieren
def extract_file_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.suffix.lower() == ".pdf":
        return extract_text(str(file_path))
    elif file_path.suffix.lower() == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

# Endpunkt: CV hochladen
@app.post("/upload-cv/")
async def upload_cv(files: List[UploadFile] = File(...)):
    return await save_files(files, CV_DIR)

# Endpunkt: Anschreiben hochladen
@app.post("/upload-letter/")
async def upload_letter(files: List[UploadFile] = File(...)):
    return await save_files(files, LETTER_DIR)

# Gemeinsame Datei-Speicherlogik
async def save_files(files: List[UploadFile], dirs: dict):
    uploaded_files = []
    for file in files:
        file_path = Path(dirs["original"]) / file.filename
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Dateiformat {file_path.suffix} wird nicht unterstützt.",
            )
        try:
            # Originaldatei speichern
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            # Textversion speichern
            text_file_path = Path(dirs["text"]) / file_path.with_suffix(".txt").name
            text_content = extract_file_text(file_path)
            if text_content:
                with open(text_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(text_content)
            uploaded_files.append({"original": str(file_path), "text": str(text_file_path)})
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Fehler beim Hochladen der Datei {file.filename}: {e}"
            )
    return {"uploaded_files": uploaded_files}
