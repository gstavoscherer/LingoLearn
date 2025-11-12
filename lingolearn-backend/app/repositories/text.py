from sqlalchemy.orm import Session

from app.models.text import Text
from app.repositories.base_repository import BaseRepository

class TextRepository(BaseRepository[Text]):
    def __init__(self, db: Session):
        super().__init__(Text, db)

