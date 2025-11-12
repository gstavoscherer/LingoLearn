from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.language import LanguageCreate, LanguageResponse, LanguageUpdate
from app.services.language import (
    create_language,
    update_language,
    get_language_by_id,
    list_languages,
    delete_language,
)

router = APIRouter(prefix="/languages", tags=["languages"])

@router.post("/", response_model=LanguageResponse, status_code=201)
def create_language_endpoint(language: LanguageCreate, db: Session = Depends(get_db)):
    return create_language(db, language)

@router.put("/{language_id}", response_model=LanguageResponse)
def update_language_endpoint(language_id: int, language: LanguageUpdate, db: Session = Depends(get_db)):
    return update_language(db, language_id, language)

@router.get("/{language_id}", response_model=LanguageResponse)
def get_language_endpoint(language_id: int, db: Session = Depends(get_db)):
    return get_language_by_id(db, language_id)

@router.get("/", response_model=list[LanguageResponse])
def list_languages_endpoint(db: Session = Depends(get_db)):
    return list_languages(db)

@router.delete("/{language_id}", status_code=204)
def delete_language_endpoint(language_id: int, db: Session = Depends(get_db)):
    return delete_language(db, language_id)
