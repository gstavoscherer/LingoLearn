import bcrypt
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from .config import settings
from .exceptions import InvalidTokenError

def hash_password(password: str) -> str:
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
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

def create_access_token(data: dict) -> str:
    try:
        expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        to_encode.update({"exp": expires})
        return jwt.encode(
            to_encode,
            settings.JWT_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
    except Exception as e:
        raise

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