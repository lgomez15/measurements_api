from fastapi import Header, HTTPException, Depends
from app.database import get_db

API_KEY = "simple-secret-key"

def check_api_key(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

def get_db_session():
    return Depends(get_db)
