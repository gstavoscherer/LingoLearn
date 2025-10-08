from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from core.security import decode_token
from sqlalchemy.orm import Session
from schemas.auth import Token, TokenResponse
from database.connection import get_db
from services.auth import authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    
    token = authenticate_user(db, email=form_data.username, password=form_data.password)
  
    return token

@router.get("/", response_model=TokenResponse)
async def validate_token(
    authorization: str = Header(...)
):
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    decoded_token = decode_token(token)

    return TokenResponse(
        sub=decoded_token["sub"],
        email=decoded_token.get("email"),
        username=decoded_token.get("username")
    )
    

