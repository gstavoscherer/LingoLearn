from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user_word import UserWordCreate, UserWordUpdate, UserWordResponse, UserWordListResponse
from app.services.user_word import (
    create_user_word,
    update_user_word,
    get_user_word,
    delete_user_word,
    list_user_words,
)
from app.core.security import get_current_user_id

router = APIRouter(prefix="/user-words", tags=["user_words"])

@router.post("", response_model=UserWordResponse, status_code=201)
def create_user_word_endpoint(data: UserWordCreate, db: Session = Depends(get_db), user_id:int = Depends(get_current_user_id)):
    data.user_id = user_id
    return create_user_word(db, data)

@router.put("/{user_id}/{word_id}", response_model=UserWordResponse)
def update_user_word_endpoint(
    user_id: int, word_id: int, data: UserWordUpdate, db: Session = Depends(get_db)
):
    return update_user_word(db, user_id, word_id, data)

@router.get("", response_model=UserWordListResponse)
def list_user_words_endpoint(
    query: str = Query(None, description="Buscar por palavra ou tradução"),
    language_id: int = Query(None, description="ID do idioma das palavras"),
    status: str = Query(None, description="Status da palavra: new, learning, known"),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(20, ge=1, description="Palavras por página"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return list_user_words(db, user_id, query, language_id, status, page, per_page)

@router.get("/{user_id}/{word_id}", response_model=UserWordResponse)
def get_user_word_endpoint(user_id: int, word_id: int, db: Session = Depends(get_db)):
    word = get_user_word(db, user_id, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found for this user.")
    return word

@router.delete("/{user_id}/{word_id}", status_code=204)
def delete_user_word_endpoint(user_id: int, word_id: int, db: Session = Depends(get_db)):
    deleted = delete_user_word(db, user_id, word_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Word not found or already deleted.")
    return None
