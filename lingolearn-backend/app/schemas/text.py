from fastapi import Form
from pydantic import BaseModel

from app.schemas.language import LanguageResponse
from app.schemas.page import PageResponse

class TextImport(BaseModel):
    title: str
    author: str
    content: str
    language_id: int
    user_id: int

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        author: str = Form(...),
        content: str = Form(...),
        language_id: str = Form(...),
        user_id: int = Form(...)
    ):
        return cls(
            title=title,
            author=author,
            content=content,
            language_id=language_id,
            user_id=user_id
        )


class TextResponse(BaseModel):
    id: int
    user_id: int
    title: str
    author: str
    image_path: str | None = None
    language: LanguageResponse | None = None
    last_visited_page: int
    total_pages: int
    total_known_words: int
    total_words: int

    class Config:
        from_attributes = True


class TextListResponse(BaseModel):
    texts: list[TextResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class TextUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    language_id: int | None = None


class TextPageResponse(BaseModel):
    text: TextResponse
    page: PageResponse

    class Config:
        from_attributes = True

    
    