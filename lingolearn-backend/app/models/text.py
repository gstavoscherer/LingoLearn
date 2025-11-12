from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel


class Text(BaseModel):
    __tablename__ = "Text"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    last_visited_page: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    total_pages: Mapped[int] = mapped_column(Integer, nullable=False)
    total_words: Mapped[int] = mapped_column(Integer, nullable=False)
    total_known_words: Mapped[int] = mapped_column(Integer, nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True)

    language_id: Mapped[int] = mapped_column(ForeignKey("Language.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)

    # Relationships
    language: Mapped["Language"] = relationship(back_populates="texts")
    user: Mapped["User"] = relationship(back_populates="texts")
    pages: Mapped[list["Page"]] = relationship(back_populates="text", cascade="all, delete-orphan")
    text_words: Mapped[list["TextWord"]] = relationship(back_populates="text", cascade="all, delete-orphan")
