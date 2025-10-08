from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class UserListResponse(BaseModel):
    users: list[UserResponse]
    count: int