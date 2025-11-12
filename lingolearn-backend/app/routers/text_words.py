from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.text_word import TextWordCreate, TextWordUpdate, TextWordResponse
from app.services.text_word import create_text_word, update_text_word

router = APIRouter(prefix="/text-words", tags=["text_words"])

@router.post("/", response_model=TextWordResponse, status_code=201)
def create_text_word_endpoint(data: TextWordCreate, db: Session = Depends(get_db)):
    return create_text_word(db, data)

@router.put("/{text_id}/{word_id}", response_model=TextWordResponse)
def update_text_word_endpoint(
    text_id: int, word_id: int, data: TextWordUpdate, db: Session = Depends(get_db)
):
    return update_text_word(db, text_id, word_id, data)
