from sqlalchemy.orm import Session
from models import Text
from .base_repository import BaseRepository

class TextRepository(BaseRepository[Text]):
    def __init__(self, db: Session):
        super().__init__(Text, db)

    