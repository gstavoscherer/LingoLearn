from fastapi import Form
from pydantic import BaseModel

class TextImport(BaseModel):
    title: str
    author: str
    content: str
    language: str
    user_id: int

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        author: str = Form(...),
        content: str = Form(...),
        language: str = Form(...),
        user_id: int = Form(...)
    ):
        return cls(
            title=title,
            author=author,
            content=content,
            language=language,
            user_id=user_id
        )

class TextResponse(BaseModel):
    id: int
    user_id: int
    title: str
    author: str
    image_path: str | None
    language: str
    total_know_words: int
    total_words: int

class TextListResponse(BaseModel):
    texts: list[TextResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


    
    