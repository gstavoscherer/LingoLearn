from sqlalchemy.orm import Session
from sqlalchemy.future import select

from app.models.text_word import TextWord
from app.repositories.base_repository import BaseRepository

class TextWordRepository(BaseRepository[TextWord]):
    def __init__(self, db: Session):
        super().__init__(TextWord, db)

    def get_by_text_id(self, text_id: int):
        stmt = select(self.model).where(self.model.text_id == text_id)
        return self.db.scalars(stmt).all()

    def get_texts_by_word_id(self, word_id: int):
        stmt = select(self.model.text_id).where(self.model.word_id == word_id)
        return self.db.scalars(stmt).all()

    def get_by_word_id(self, word_id: int):
        stmt = select(self.model).where(self.model.word_id == word_id)
        return self.db.scalars(stmt).all()
    
    def bulk_create(self, text_words_data):
        text_words_objects = [
            TextWord(
                text_id=data['text_id'],
                word_id=data['word_id'], 
                quantity=data['quantity']
            )
            for data in text_words_data
        ]
        self.db.add_all(text_words_objects)
        self.db.commit()
