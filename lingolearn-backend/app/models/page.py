from sqlalchemy import Integer, Text as TextType, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel


class Page(BaseModel):
    __tablename__ = "Page"

    number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(TextType, nullable=False)
    text_id: Mapped[int] = mapped_column(ForeignKey("Text.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("text_id", "number"),
    )

    # Relationships
    text: Mapped["Text"] = relationship(back_populates="pages")
