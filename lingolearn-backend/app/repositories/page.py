from sqlalchemy.orm import Session

from app.models.page import Page
from app.repositories.base_repository import BaseRepository

class PageRepository(BaseRepository[Page]):
    def __init__(self, db: Session):
        super().__init__(Page, db)