from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.word import WordRepository
from app.schemas.word import WordCreate, WordUpdate, WordResponse

ALLOWED_FIELDS = {"word", "language_id"}

def create_word(db: Session, data: WordCreate) -> WordResponse:
    try:
        repo = WordRepository(db)
        new = repo.create(**data.model_dump())
        db.commit()
        db.refresh(new)
        return WordResponse(id=new.id, word=new.word, language_id=new.language_id)
    except Exception:
        db.rollback()
        raise

def update_word(db: Session, word_id: int, data: WordUpdate) -> WordResponse:
    try:
        repo = WordRepository(db)
        word = repo.get(word_id)
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        patch = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in patch.items():
            if field in ALLOWED_FIELDS:
                setattr(word, field, value)

        db.commit()
        db.refresh(word)
        return WordResponse(id=word.id, word=word.word, language_id=word.language_id)
    except Exception:
        db.rollback()
        raise

def get_word(db: Session, word_id: int = None, word: str = None, language_id = None) -> WordResponse:
    word_repo = WordRepository(db)
    if word_id:
        word = word_repo.get(word_id)
    else:
        word = word_repo.get_by(word=word, language_id=language_id)

    return WordResponse.model_validate(word)
