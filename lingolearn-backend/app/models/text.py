
from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer  

class Text(BaseModel):
    __tablename__ = "Text"

    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    total_know_words: Mapped[int] = mapped_column(Integer, default=0)
    total_words: Mapped[int] = mapped_column(Integer)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True)
    #Relationships
    pages: Mapped[list["Page"]] = relationship(back_populates="text")
    words: Mapped[list["TextWord"]] = relationship(back_populates="text")
    user: Mapped["User"] = relationship(back_populates="texts")