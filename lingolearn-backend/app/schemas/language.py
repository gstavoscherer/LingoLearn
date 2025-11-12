from pydantic import BaseModel, StringConstraints
from typing import Annotated

class LanguageCreate(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)]
    code: Annotated[str, StringConstraints(max_length=10)]


class LanguageUpdate(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50)] | None = None
    code: Annotated[str, StringConstraints(max_length=10)] | None = None


class LanguageResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True


class LanguageListResponse(BaseModel):
    languages: list[LanguageResponse]
    count: int
