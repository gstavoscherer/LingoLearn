from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

class TextWord(BaseModel):
    __tablename__ = "TextWord"

    text_id: Mapped[int] = mapped_column(ForeignKey("Text.id"))
    normalized: Mapped[str] = mapped_column(String(100))
    appearance_count: Mapped[int] = mapped_column(Integer)

    #Relationships
    text: Mapped["Text"] = relationship(back_populates="words")