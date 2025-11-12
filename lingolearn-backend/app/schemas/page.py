from pydantic import BaseModel, constr

class PageCreate(BaseModel):
    text_id: int
    number: int
    content: constr(min_length=1)

class PageUpdate(BaseModel):
    content: str | None = None

class PageResponse(BaseModel):
    id: int
    text_id: int
    number: int
    content: str
    class Config:
        from_attributes = True

class PageListResponse(BaseModel):
    pages: list[PageResponse]
    count: int
