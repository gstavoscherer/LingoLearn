from sqlalchemy.orm import Session
from app.models.language import Language
from app.repositories.base_repository import BaseRepository

class LanguageRepository(BaseRepository[Language]):
    def __init__(self, db: Session):
        super().__init__(Language, db)
