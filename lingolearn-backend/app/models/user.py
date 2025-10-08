from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = "User"
    
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(127))

    #Relationship
    texts: Mapped[list["Text"]] = relationship(back_populates="user")
    words: Mapped[list["UserWord"]] = relationship(back_populates="user")