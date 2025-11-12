from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.user_word import UserWordRepository
from app.schemas.user_word import (
    UserWordCreate,
    UserWordUpdate,
    UserWordResponse,
    UserWordListResponse,
    PaginatedList,
)

ALLOWED_FIELDS = {
    "easiness_factor",
    "translation",
    "translation_language_id",
    "context",
    "last_review",
    "next_review",
}



def create_user_word(db: Session, data: UserWordCreate) -> UserWordResponse:
    try:
        repo = UserWordRepository(db)

        user_word = repo.create(**data.model_dump())

        db.commit()
        db.refresh(user_word, ["word"])
        return UserWordResponse.model_validate(user_word)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating or updating UserWord: {e}"
        )

def update_user_word(db: Session, user_id: int, word_id: int, data: UserWordUpdate) -> UserWordResponse:
    try:
        repo = UserWordRepository(db)
        user_word = repo.get_by_user_and_word(user_id=user_id, word_id=word_id)
        if not user_word:
            raise HTTPException(status_code=404, detail="UserWord not found")

        patch = data.model_dump(exclude_unset=True, exclude_none=True)
        for f, v in patch.items():
            if f in ALLOWED_FIELDS:
                setattr(user_word, f, v)

        db.commit()
        db.refresh(user_word)
        return UserWordResponse.model_validate(user_word)
    except Exception:
        db.rollback()
        raise


def list_user_words(
    db: Session, 
    user_id: int,
    query: str = None, 
    language_id: int = None, 
    status: str = None, 
    page: int = 1, 
    per_page: int = 20
) -> UserWordListResponse:
    user_word_repo = UserWordRepository(db)
    
    # Calcular offset para paginação
    offset = (page - 1) * per_page
    
    # Buscar palavras com filtros
    results, total_count = user_word_repo.get_user_words_paginated(
        user_id=user_id, 
        query=query,  # Novo filtro
        language_id=language_id, 
        status=status,
        limit=per_page, 
        offset=offset
    )
    
    # Calcular estatísticas
    stats = user_word_repo.get_user_words_stats(
        user_id=user_id, 
        query=query,  # Novo filtro
        language_id=language_id
    )
    
    # Calcular total de páginas
    total_pages = (total_count + per_page - 1) // per_page
    
    # Converter para response
    user_words_response = [
        UserWordResponse.model_validate(word)
        for word in results
    ]
    
    # Construir resposta paginada
    pagination = PaginatedList[UserWordResponse](
        items=user_words_response,
        current_page=page,
        total_pages=total_pages,
        per_page=per_page,
        total_count=total_count
    )
    
    return UserWordListResponse(
        pagination=pagination,
        stats=stats
    )




def get_user_word(db: Session, user_id: int, word_id: int) -> UserWordResponse | None:
    repo = UserWordRepository(db)
    user_word = repo.get_by_user_and_word(user_id=user_id, word_id=word_id)
    if not user_word:
        raise HTTPException(status_code=404, detail="UserWord not found")

    return UserWordResponse.model_validate(user_word)


def delete_user_word(db: Session, user_id: int, word_id: int) -> bool:
    try:
        repo = UserWordRepository(db)
        user_word = repo.get_by_user_and_word(user_id=user_id, word_id=word_id)
        if not user_word:
            return False
        
        repo.delete(user_word)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
