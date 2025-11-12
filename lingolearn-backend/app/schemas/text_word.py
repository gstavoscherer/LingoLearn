from pydantic import BaseModel

class TextWordCreate(BaseModel):
    text_id: int
    word_id: int
    quantity: int

class TextWordUpdate(BaseModel):
    quantity: int | None = None

class TextWordResponse(BaseModel):
    text_id: int
    word_id: int
    quantity: int
    class Config:
        from_attributes = True

class TextWordListResponse(BaseModel):
    text_words: list[TextWordResponse]
    count: int
