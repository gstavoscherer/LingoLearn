from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import re
from app.core.security import hash_password, decode_token, verify_password
from datetime import timedelta
from app.core.config import settings
from app.core.security import decode_token, create_access_token, hash_password
from app.schemas.auth import Token, TokenResponse, PasswordResetRequest, PasswordResetConfirm
from app.schemas.user import UserResponse
from app.database.connection import get_db
from app.services.auth import authenticate_user
from app.repositories.user import UserRepository
from app.core.mailer import send_email

router = APIRouter(prefix="/auth", tags=["Authentication"])
RESET_TOKEN_EXPIRE_MINUTES = 15

@router.post("/", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password
    )
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
        username=decoded_token.get("username"),
        last_visited_text_id=(
            int(decoded_token["last_visited_text_id"])
            if decoded_token.get("last_visited_text_id") is not None
            else None
        ),
        translation_language_id = (
            int(decoded_token["translation_language_id"])
        ),
        translation_language_name=decoded_token.get("translation_language_name"),
    )


@router.post("/request-password-reset")
async def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by(email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email."
        )

    token_data = {"sub": str(user.id), "email": user.email, "action": "reset_password"}
    reset_token = create_access_token(token_data, expires_delta=timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES))
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    subject = "Password Reset Request"
    body = (
        f"Hi {user.username},\n\n"
        f"Use the link below to reset your password (valid for {RESET_TOKEN_EXPIRE_MINUTES} minutes):\n\n"
        f"{reset_link}\n\n"
        f"If you didn’t request this, please ignore this message."
    )

    try:
        send_email(to=user.email, subject=subject, body=body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

    return {"detail": "Password reset link sent to your email."}

@router.post("/confirm-password-reset", response_model=UserResponse)
async def confirm_password_reset(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    try:
        payload = decode_token(data.token)
        if payload.get("action") != "reset_password":
            raise HTTPException(status_code=400, detail="Invalid reset token.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid or expired token: {str(e)}")

    user_repo = UserRepository(db)
    user = user_repo.get(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    new_password = data.new_password

    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", new_password):
        raise HTTPException(status_code=400, detail="Password must contain an uppercase letter.")
    if not re.search(r"[a-z]", new_password):
        raise HTTPException(status_code=400, detail="Password must contain a lowercase letter.")
    if not re.search(r"\d", new_password):
        raise HTTPException(status_code=400, detail="Password must contain a number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
        raise HTTPException(status_code=400, detail="Password must contain a special character.")

    # 🚫 Verifica se a nova senha é igual à antiga
    if verify_password(new_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="New password cannot be the same as the old password."
        )

    try:
        user.password = hash_password(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while resetting password: {str(e)}"
        )
