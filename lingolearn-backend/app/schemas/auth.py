from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenResponse(BaseModel):
    sub: str
    username: str
    email: str
    last_visited_text_id: int | None
    translation_language_id: int | None
    translation_language_name: str | None

class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


