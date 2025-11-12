from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.language import get_language_by_id
from app.schemas.translate import TranslateResponse
from app.database.connection import get_db

from googletrans import Translator

router = APIRouter(prefix="/translate", tags=["translate"])

@router.get("", response_model=TranslateResponse)
async def translate_endpoint(word: str, src_language_id: int, dest_language_id: int, db: Session = Depends(get_db)):
    async with Translator() as translator:
        src_language = get_language_by_id(db, src_language_id)
        dest_language = get_language_by_id(db, dest_language_id)

        result = await translator.translate(word, src=src_language.code, dest=dest_language.code)

        return TranslateResponse(dest=dest_language.name, src=src_language.name, translation=result.text)