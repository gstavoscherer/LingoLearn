from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel


class Word(BaseModel):
    __tablename__ = "Word"

    word: Mapped[str] = mapped_column(String(100), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("Language.id"), nullable=False)

    # Relationships
    language: Mapped["Language"] = relationship(back_populates="words")
    user_words: Mapped[list["UserWord"]] = relationship(back_populates="word")
    text_words: Mapped[list["TextWord"]] = relationship(back_populates="word")
