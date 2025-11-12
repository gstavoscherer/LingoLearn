from pydantic import BaseModel

class TranslateResponse(BaseModel):
    src: str
    dest: str
    translation: str