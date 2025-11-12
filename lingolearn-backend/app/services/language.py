from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.language import LanguageRepository
from app.schemas.language import LanguageCreate, LanguageResponse, LanguageUpdate


ALLOWED_FIELDS = {"name", "code"}


def create_language(db: Session, lang_data: LanguageCreate) -> LanguageResponse:
    try:
        repo = LanguageRepository(db)

        if repo.get_by(code=lang_data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Language with code '{lang_data.code}' already exists.",
            )

        new_language = repo.create(**lang_data.model_dump())
        db.commit()
        db.refresh(new_language)

        return LanguageResponse(
            id=new_language.id,
            name=new_language.name,
            code=new_language.code,
        )

    except Exception:
        db.rollback()
        raise


def update_language(db: Session, lang_id: int, lang_data: LanguageUpdate) -> LanguageResponse:
    try:
        repo = LanguageRepository(db)

        language = repo.get(lang_id)
        if not language:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Language not found",
            )

        patch = lang_data.model_dump(exclude_unset=True, exclude_none=True)
        patch = {k: v for k, v in patch.items() if k in ALLOWED_FIELDS}

        if not patch:
            return LanguageResponse(
                id=language.id, name=language.name, code=language.code
            )

        for field, value in patch.items():
            setattr(language, field, value)

        db.add(language)
        db.commit()
        db.refresh(language)

        return LanguageResponse(
            id=language.id,
            name=language.name,
            code=language.code,
        )

    except Exception:
        db.rollback()
        raise


def get_language_by_id(db: Session, lang_id: int) -> LanguageResponse:
    repo = LanguageRepository(db)
    language = repo.get(lang_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return LanguageResponse.from_orm(language)


def list_languages(db: Session) -> list[LanguageResponse]:
    repo = LanguageRepository(db)
    langs = repo.list_all()
    return [LanguageResponse.from_orm(l) for l in langs]


def delete_language(db: Session, lang_id: int):
    try:
        repo = LanguageRepository(db)
        language = repo.get(lang_id)
        if not language:
            raise HTTPException(status_code=404, detail="Language not found")

        repo.delete(language)
        db.commit()

    except Exception:
        db.rollback()
        raise
