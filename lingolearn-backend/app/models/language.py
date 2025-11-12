from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel


class Language(BaseModel):
    __tablename__ = "Language"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    # Relationships
    words: Mapped[list["Word"]] = relationship(back_populates="language")
    user_words_translation: Mapped[list["UserWord"]] = relationship(
        back_populates="translation_language"
    )
    texts: Mapped[list["Text"]] = relationship(back_populates="language")
