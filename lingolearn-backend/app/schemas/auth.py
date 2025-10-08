from pydantic import  BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenResponse(BaseModel):
    sub: str
    username: str
    email: str


