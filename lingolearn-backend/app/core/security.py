import bcrypt
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.exceptions import InvalidTokenError

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status


security = HTTPBearer()

def hash_password(password: str) -> str:
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed)
        return hashed.decode('utf-8')

    except Exception as e:
        raise ValueError("Falha ao processar senha")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT token.
    If expires_delta is not provided, defaults to ACCESS_TOKEN_EXPIRE_MINUTES from settings.
    """
    try:
        to_encode = data.copy()

        # Usa o tempo padrão se não for passado nada
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    except Exception as e:
        raise RuntimeError(f"Error creating access token: {str(e)}")

def decode_token(token: str) -> dict:
    """Valida e decodifica um token JWT."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise InvalidTokenError(message="Token expirado")
    except JWTError as e:
        raise InvalidTokenError(message="Token inválido")

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Obtém o usuário atual a partir do token JWT.
    """
    try:
        token = credentials.credentials
        payload = decode_token(token)

        user = payload.get("sub") or payload.get("user_id")
        return int(user)

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.message)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
