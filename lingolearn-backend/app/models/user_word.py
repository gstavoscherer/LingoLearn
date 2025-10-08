from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, UniqueConstraint
from enum import Enum
from sqlalchemy import Enum as SQLEnum  

class WordStatus(Enum):
    UNKNOW = 1
    RECOGNIZE = 2
    FAMILIAR = 3
    WELLKNOW = 4
    KNOW = 5

class UserWord(BaseModel):
    __tablename__ = "UserWord"

    status: Mapped[WordStatus] = mapped_column(SQLEnum(WordStatus), nullable=False, default=WordStatus.UNKNOW)
    original: Mapped[str] = mapped_column(String(100), nullable=False)
    tranlation: Mapped[str] = mapped_column(String(100))
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))

    __table_args__ = (
        UniqueConstraint("original", "language"),
    )

    #Relationships
    user: Mapped["User"] = relationship(back_populates="words")
