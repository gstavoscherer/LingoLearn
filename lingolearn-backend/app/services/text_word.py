from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.text_word import TextWordRepository
from app.schemas.text_word import TextWordCreate, TextWordUpdate, TextWordResponse

def create_text_word(db: Session, data: TextWordCreate) -> TextWordResponse:
    try:
        repo = TextWordRepository(db)
        new = repo.create(**data.model_dump())
        db.commit()
        db.refresh(new)
        return TextWordResponse(text_id=new.text_id, word_id=new.word_id, quantity=new.quantity)
    except Exception:
        db.rollback()
        raise

def update_text_word(db: Session, text_id: int, word_id: int, data: TextWordUpdate) -> TextWordResponse:
    try:
        repo = TextWordRepository(db)
        tw = repo.get(text_id=text_id, word_id=word_id)
        if not tw:
            raise HTTPException(status_code=404, detail="TextWord not found")

        patch = data.model_dump(exclude_unset=True, exclude_none=True)
        if "quantity" in patch:
            tw.quantity = patch["quantity"]

        db.commit()
        db.refresh(tw)
        return TextWordResponse(text_id=tw.text_id, word_id=tw.word_id, quantity=tw.quantity)
    except Exception:
        db.rollback()
        raise
