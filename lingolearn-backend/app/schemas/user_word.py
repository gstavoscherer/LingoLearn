from pydantic import BaseModel, Field
from datetime import date
from typing import Annotated, Generic, TypeVar, List

from app.schemas.word import WordResponse

T = TypeVar('T')

class UserWordCreate(BaseModel):
    user_id: int | None = None
    word_id: int
    easiness_factor: Annotated[float, Field(gt=0)] = 1.5
    translation: Annotated[str, Field(max_length=100)]
    translation_language_id: int
    context: Annotated[str, Field(max_length=255)]
    context_translation: Annotated[str, Field(max_length=255)]
    last_review: date | None = None
    next_review: date | None = None

class UserWordUpdate(BaseModel):
    easiness_factor: Annotated[float, Field(gt=0)] = 1.5
    translation: str | None = None
    translation_language_id: int | None = None
    context: str | None = None
    last_review: date | None = None
    next_review: date | None = None

class UserWordResponse(BaseModel):
    user_id: int
    word: WordResponse
    translation: str
    translation_language_id: int
    easiness_factor: float
    context: str
    context_translation: str
    last_review: date | None = None
    next_review: date | None = None

    class Config:
        from_attributes = True

class UserWordListResponse(BaseModel):
    user_words: list[UserWordResponse]
    count: int

class WordStats(BaseModel):
    total: int
    known: int
    learning: int
    new: int

class PaginatedList(BaseModel, Generic[T]):
    items: List[T]
    current_page: int
    total_pages: int
    per_page: int
    total_count: int

class UserWordListResponse(BaseModel):
    pagination: PaginatedList[UserWordResponse]
    stats: WordStats
