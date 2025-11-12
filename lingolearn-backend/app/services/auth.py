from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.schemas.auth import Token
from app.core.security import verify_password, create_access_token
from app.core.exceptions import AuthenticationError
from datetime import datetime, timedelta
from app.repositories.user import UserRepository

def authenticate_user(db: Session, email: EmailStr, password: str) -> Token:
    user = UserRepository(db).get_by(email=email)
    now = datetime.utcnow()
    print("User attempting to authenticate:", email)

    if not user or not verify_password(password, user.password):
        raise AuthenticationError(email)
    print("User authenticated successfully:", email)
     # ⚡ Lógica do streak
    if user.last_login:
        days_diff = (now.date() - user.last_login.date()).days
        if days_diff == 1:
            user.streak += 1  # ✅ login no dia seguinte → incrementa
        elif days_diff > 1:
            user.streak = 1   # 🧊 perdeu o streak
    else:
        user.streak = 1       # 🔥 primeiro login
    print(f"User {email} streak updated to {user.streak}")
    user.last_login = now
    db.commit()
    db.refresh(user)
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "username": user.username,
        "last_visited_text_id": user.last_visited_text_id or None,
        "translation_language_id": user.translation_language_id or None
    }

    access_token = create_access_token(token_data)
    if not access_token:
        raise AuthenticationError(email)

    token = {
        "access_token": access_token,
        "token_type": "bearer"
        }
    return token
