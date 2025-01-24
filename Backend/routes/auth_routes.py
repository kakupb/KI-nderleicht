from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

router = APIRouter(prefix="/auth", tags=["Auth"])

# Dummy-Admin-Daten
ADMIN_USERNAME = "yakupb"
ADMIN_PASSWORD = "hhhhhhhh"
API_KEY = "supersecureapikey"

# Header für Admin-Authentifizierung
api_key_header = APIKeyHeader(name="Authorization")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == ADMIN_USERNAME and form_data.password == ADMIN_PASSWORD:
        return {"message": "Erfolgreich eingeloggt", "api_key": API_KEY}
    raise HTTPException(status_code=401, detail="Ungültige Anmeldedaten")

def verify_admin(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Zugriff verweigert")
    return True
