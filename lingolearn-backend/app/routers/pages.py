from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.page import PageCreate, PageResponse, PageUpdate
from app.services.page import create_page, update_page

router = APIRouter(prefix="/pages", tags=["pages"])

@router.post("/", response_model=PageResponse, status_code=201)
def create_page_endpoint(page: PageCreate, db: Session = Depends(get_db)):
    return create_page(db, page)

@router.put("/{page_id}", response_model=PageResponse)
def update_page_endpoint(page_id: int, page: PageUpdate, db: Session = Depends(get_db)):
    return update_page(db, page_id, page)
