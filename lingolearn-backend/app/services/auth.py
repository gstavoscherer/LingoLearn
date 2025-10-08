from pydantic import EmailStr
from schemas.auth import Token
from core.security import verify_password, create_access_token
from core.exceptions import AuthenticationError
from repositories import UserRepository
from sqlalchemy.orm import Session

def authenticate_user(db: Session, email: EmailStr, password: str) -> Token:
    user = UserRepository(db).get_by(email=email)
    
    if not user or not verify_password(password, user.password):
        raise AuthenticationError(email)

    token_data = {"sub": str(user.id), "email": user.email, "username": user.username}

    access_token = create_access_token(token_data)
    if not access_token:
        raise AuthenticationError(email)

    token = {
        "access_token": access_token,
        "token_type": "bearer"
        } 
    return token