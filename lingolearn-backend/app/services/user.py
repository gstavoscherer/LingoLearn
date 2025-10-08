from fastapi import HTTPException, status
from core.security import hash_password
from core.exceptions import UserAlreadyExistsError
from repositories.user import UserRepository
from schemas.user import UserCreate, UserResponse, UserUpdate
from sqlalchemy.orm import Session
ALLOWED_FIELDS = {"username", "email", "password"}

def register_user(db: Session, user_data: UserCreate) -> UserResponse:
    try:
        user_repo = UserRepository(db)

        if user_repo.get_by(email=user_data.email):
            raise UserAlreadyExistsError(email=user_data.email)
        
        user_to_create = {
            "username": user_data.username,
            "email": user_data.email,
            "password": hash_password(user_data.password)
        }
        
        new_user = user_repo.create(**user_to_create)
        
        db.commit()
        db.refresh(new_user)

        user_response = UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username
        )
        
        return user_response
    except Exception:
        db.rollback()
        raise


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> UserResponse:
    """
    Partially updates the user. Only fields present in the payload are changed.
    Fields not sent remain untouched. Password is hashed only if provided.
    """
    try:
        user_repo = UserRepository(db)

        user = user_repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        patch = user_data.model_dump(exclude_unset=True, exclude_none=True)

        patch = {k: v for k, v in patch.items() if k in ALLOWED_FIELDS}

        if not patch:
            return UserResponse(id=user.id, email=user.email, username=user.username)

        if "password" in patch:
            patch["password"] = hash_password(patch["password"])

        for field, value in patch.items():
            setattr(user, field, value)

        db.add(user)
        db.commit()
        db.refresh(user)

        return UserResponse(id=user.id, email=user.email, username=user.username)

    except Exception:
        db.rollback()
        raise