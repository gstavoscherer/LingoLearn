from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.word import WordCreate, WordResponse, WordUpdate
from app.services.word import create_word, update_word, get_word

router = APIRouter(prefix="/words", tags=["words"])

@router.post("", response_model=WordResponse, status_code=201)
def create_word_endpoint(word: WordCreate, db: Session = Depends(get_db)):
    return create_word(db, word)

@router.put("/{word_id}", response_model=WordResponse)
def update_word_endpoint(word_id: int, word: WordUpdate, db: Session = Depends(get_db)):
    return update_word(db, word_id, word)

@router.get("", response_model=WordResponse)
def get_word_endpoint(
    word_id: int = None,
    word: str = None,
    language_id: int = None,
    db: Session = Depends(get_db)
):
    return get_word(db, word_id, word, language_id)
