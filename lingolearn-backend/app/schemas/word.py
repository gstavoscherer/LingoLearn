from pydantic import BaseModel, constr

class WordCreate(BaseModel):
    word: constr(max_length=100)
    language_id: int

class WordUpdate(BaseModel):
    word: constr(max_length=100) | None = None
    language_id: int | None = None

class WordResponse(BaseModel):
    id: int
    word: str
    language_id: int
    class Config:
        from_attributes = True

class WordListResponse(BaseModel):
    words: list[WordResponse]
    count: int
