from sqlalchemy.orm import Session
from app.models.word import Word
from app.repositories.base_repository import BaseRepository

class WordRepository(BaseRepository[Word]):
    def __init__(self, db: Session):
        super().__init__(Word, db)
    
    def get_words_by_list(self, words_list, language_id):
        return self.db.query(Word).filter(
            Word.word.in_(words_list),
            Word.language_id == language_id
        ).all()

    def bulk_create(self, words_list, language_id):
        words_objects = [
            Word(word=word, language_id=language_id) 
            for word in words_list
        ]
        self.db.add_all(words_objects)
        self.db.flush()
        return words_objects

