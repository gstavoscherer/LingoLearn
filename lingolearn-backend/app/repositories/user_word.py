from sqlalchemy.orm import Session
from models import UserWord
from .base_repository import BaseRepository

class UserWordRepository(BaseRepository[UserWord]):
    def __init__(self, db: Session):
        super().__init__(UserWord, db)

    