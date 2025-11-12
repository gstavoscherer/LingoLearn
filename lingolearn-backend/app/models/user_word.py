from sqlalchemy import String, Float, Date, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from app.models.base_model import BaseModelForRelationships


class UserWord(BaseModelForRelationships):
    __tablename__ = "User_Word"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("Word.id"), primary_key=True)

    easiness_factor: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)
    translation: Mapped[str] = mapped_column(String(100), nullable=False)
    translation_language_id: Mapped[int] = mapped_column(
        ForeignKey("Language.id"), nullable=False
    )
    context: Mapped[str] = mapped_column(String(255), nullable=False)
    context_translation: Mapped[str] = mapped_column(String(255), nullable=False)
    last_review: Mapped[Date] = mapped_column(Date, nullable=True)
    next_review: Mapped[Date] = mapped_column(Date, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="user_words")
    word: Mapped["Word"] = relationship(back_populates="user_words")
    translation_language: Mapped["Language"] = relationship(
        back_populates="user_words_translation"
    )

# Trigger para atualizar o total de palavras conhecidas
@event.listens_for(UserWord, 'after_insert')
def increment_known_words_after_insert(mapper, connection, target):
    from app.models import Text, TextWord

    session = Session.object_session(target)
    
    if session is None:
        return
    
    # Buscar todos os text_ids que contêm esta palavra
    text_words = session.query(TextWord.text_id).filter(
        TextWord.word_id == target.word_id
    ).all()
    
    text_ids = [tw.text_id for tw in text_words]
    
    if text_ids:
        # Bulk update - mais eficiente
        session.query(Text).filter(
            Text.id.in_(text_ids)
        ).update(
            {Text.total_known_words: Text.total_known_words + 1},
            synchronize_session=False
        )

# Trigger para atualizar o total de palavras conhecidas
@event.listens_for(UserWord, 'after_delete')
def decrement_known_words_after_delete(mapper, connection, target):
    from app.models import Text, TextWord
    
    session = Session.object_session(target)
    
    if session is None:
        return
    
    # Buscar todos os text_ids que contêm esta palavra
    text_words = session.query(TextWord.text_id).filter(
        TextWord.word_id == target.word_id
    ).all()
    
    text_ids = [tw.text_id for tw in text_words]
    
    if text_ids:
        # Bulk update - subtrair 1
        session.query(Text).filter(
            Text.id.in_(text_ids)
        ).update(
            {Text.total_known_words: Text.total_known_words - 1},
            synchronize_session=False
        )
