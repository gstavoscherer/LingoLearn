from sqlalchemy.orm import Session
from models import TextWord
from .base_repository import BaseRepository

class TextWordRepository(BaseRepository[TextWord]):
    def __init__(self, db: Session):
        super().__init__(TextWord, db)

    