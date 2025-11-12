from datetime import datetime, timedelta
from sqlalchemy import DateTime, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "User"

    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    translation_language_id: Mapped[int] = mapped_column(Integer, nullable=False)
    last_visited_text_id: Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    study_time_in_seconds: Mapped[int] = mapped_column(Integer, nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime,nullable=True)
    streak: Mapped[int] = mapped_column(Integer, default=1)
    # Relationships
    texts: Mapped[list["Text"]] = relationship(back_populates="user")
    user_words: Mapped[list["UserWord"]] = relationship(back_populates="user")
