import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    translation_language_id: int

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    translation_language_id: int | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    translation_language_id: int | None  # Permitir valores nulos
    last_visited_text_id: int | None  # Permitir valores nulos
    is_active: bool | None  # Permitir valores nulos
    study_time_in_seconds: int | None  # Permitir valores nulos
    last_login: datetime | None  # Permitir valores nulos
    streak: int | None  # Permitir valores nulos

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]
    count: int
