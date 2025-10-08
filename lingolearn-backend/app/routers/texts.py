import sys

from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy.orm import Session
from services.text import import_text, get_text_list
from schemas.text import TextImport, TextResponse, TextListResponse
from database.connection import get_db

router = APIRouter(prefix="/texts", tags=["texts"])

@router.post("/", response_model=TextResponse, status_code=201)
def create_text_endpoint(
        text: TextImport = Depends(TextImport.as_form),
        image: UploadFile | None = File(None),
        db: Session = Depends(get_db)
):
    return import_text(db, text, image)

@router.get("/", response_model=TextListResponse)
def list_texts(
    user_id: int,
    page: int = 1,
    top: int = 10,
    query: str = '',
    db: Session = Depends(get_db)
):
    return get_text_l-+ist(db=db, user_id=user_id, top=top, page=page, query=query)
   