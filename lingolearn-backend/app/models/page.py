
from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint  

class Page(BaseModel):
    __tablename__ = "Page"

    text_id: Mapped[int] = mapped_column(ForeignKey("Text.id"))
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint("text_id", "number"),
    )

    #Relationships
    text: Mapped["Text"] = relationship(back_populates="pages")