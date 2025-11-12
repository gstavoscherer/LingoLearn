from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.page import PageRepository
from app.schemas.page import PageCreate, PageUpdate, PageResponse

def create_page(db: Session, data: PageCreate) -> PageResponse:
    try:
        repo = PageRepository(db)
        new = repo.create(**data.model_dump())
        db.commit()
        db.refresh(new)
        return PageResponse(id=new.id, text_id=new.text_id, number=new.number, content=new.content)
    except Exception:
        db.rollback()
        raise

def update_page(db: Session, page_id: int, data: PageUpdate) -> PageResponse:
    try:
        repo = PageRepository(db)
        page = repo.get(page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page not found")

        patch = data.model_dump(exclude_unset=True, exclude_none=True)
        if "content" in patch:
            page.content = patch["content"]

        db.commit()
        db.refresh(page)
        return PageResponse(id=page.id, text_id=page.text_id, number=page.number, content=page.content)
    except Exception:
        db.rollback()
        raise
