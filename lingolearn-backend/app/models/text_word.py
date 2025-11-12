from sqlalchemy import Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModelForRelationships


class TextWord(BaseModelForRelationships):
    __tablename__ = "Text_Word"

    text_id: Mapped[int] = mapped_column(ForeignKey("Text.id"), primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("Word.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    text: Mapped["Text"] = relationship(back_populates="text_words")
    word: Mapped["Word"] = relationship(back_populates="text_words")
