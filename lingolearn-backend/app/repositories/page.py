from sqlalchemy.orm import Session
from models import Page
from .base_repository import BaseRepository

class PageRepository(BaseRepository[Page]):
    def __init__(self, db: Session):
        super().__init__(Page, db)

    