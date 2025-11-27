from typing import Optional

from fastapi import APIRouter, Depends, UploadFile
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.services.user import update_user_last_visited_text
from app.services.text import import_text, get_text_list, get_text_by_id, update_text, delete_text, text_page, update_last_page
from app.schemas.text import TextImport, TextResponse, TextListResponse, TextUpdate, TextPageResponse
from app.database.connection import get_db

router = APIRouter(prefix="/texts", tags=["texts"])

@router.post("", response_model=TextResponse, status_code=201)
async def create_text_endpoint(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # max size = 10MB
        form = await request.form(max_part_size=10 * 1024 * 1024)
    except Exception as e:
        raise HTTPException(status_code=413, detail=str(e))

    # Form fields
    title = form.get("title")
    author = form.get("author")
    content = form.get("content")
    language_id = form.get("language_id")
    user_id = form.get("user_id")

    image: UploadFile | None = form.get("image")

    text = TextImport(
        title=title,
        author=author,
        content=content,
        language_id=int(language_id),
        user_id=int(user_id)
    )

    return import_text(db, text, image)

@router.get("/{text_id}")
def get_text_endpoint(
    text_id: int,
    db: Session = Depends(get_db)
):
    return get_text_by_id(db, text_id)

@router.get("/", response_model=TextListResponse)
def list_texts(
    user_id: int,
    language_id: Optional[int] = None,
    page: int = 1,
    top: int = 5,
    query: str = '',
    order_by: str = 'ascending',
    db: Session = Depends(get_db)
):
    return get_text_list(db=db, user_id=user_id, top=top, page=page, query=query, language_id=language_id, order_by=order_by)

@router.put("/{text_id}", response_model=TextResponse)
def update_text_endpoint(
    text_id: int, data: TextUpdate, db: Session = Depends(get_db)
):
    return update_text(db, data, text_id)

@router.delete("/{text_id}", status_code=204)
def delete_text_endpoint(text_id: int, db: Session = Depends(get_db)):
    return delete_text(db, text_id)

@router.get("/{text_id}/pages/{page_number}", response_model=TextPageResponse)
def text_page_endpoint(text_id: int, page_number: int, db: Session = Depends(get_db)):
    return text_page(db, text_id, page_number)

@router.post("/{text_id}/track-page", status_code=204)
def track_page_access(
    text_id: int,
    page_number: int,
    user_id = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    update_user_last_visited_text(db, user_id, text_id)
    update_last_page(db, text_id, page_number)