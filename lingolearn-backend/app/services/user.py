from hmac import new
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models import user
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.exceptions import UserAlreadyExistsError

ALLOWED_FIELDS = {"username", "email", "password", "translation_language_id"}


# -----------------------------
# CREATE USER
# -----------------------------
def register_user(db: Session, user_data: UserCreate) -> UserResponse:
    """
    Creates a new user with hashed password and duplicate email validation.
    """
    user_repo = UserRepository(db)

    if user_repo.get_by(email=user_data.email):
        raise UserAlreadyExistsError()

    user_to_create = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "translation_language_id": user_data.translation_language_id
    }
    print(user_to_create)

    try:
        new_user = user_repo.create(**user_to_create)
        db.commit()
        db.refresh(new_user)
        print(new_user)
        return UserResponse.model_validate(new_user)

    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint" in str(e.orig) or "duplicate key" in str(e.orig):
            raise UserAlreadyExistsError()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(e.orig)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while creating user: {str(e)}"
        )


# -----------------------------
# READ USER (BY ID)
# -----------------------------
def get_user_by_id(db: Session, user_id: int) -> UserResponse:
    """
    Returns a user by ID, or raises 404 if not found.
    """
    user_repo = UserRepository(db)
    user = user_repo.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.model_validate(user)


# -----------------------------
# LIST USERS
# -----------------------------
def list_users(db: Session) -> list[UserResponse]:
    """
    Returns all users in the database.
    """
    user_repo = UserRepository(db)
    users = user_repo.list_all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )

    return [
        UserResponse.model_validate(u)
        for u in users
    ]


# -----------------------------
# UPDATE USER
# -----------------------------
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> UserResponse:
    """
    Partially updates a user. Only provided fields are updated.
    Password is rehashed if present.
    """
    user_repo = UserRepository(db)
    user = user_repo.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    patch = user_data.model_dump(exclude_unset=True, exclude_none=True)
    patch = {k: v for k, v in patch.items() if k in ALLOWED_FIELDS}

    if not patch:
        return UserResponse.model_validate(user)

    if "password" in patch:
        patch["password"] = hash_password(patch["password"])

    for field, value in patch.items():
        setattr(user, field, value)

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username
        )

    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint" in str(e.orig) or "duplicate key" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered to another user."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(e.orig)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while updating user: {str(e)}"
        )


# -----------------------------
# DELETE USER
# -----------------------------
def delete_user(db: Session, user_id: int) -> dict:
    """
    Deletes a user by ID. Raises 404 if not found.
    Handles integrity errors (e.g., foreign key constraints).
    """
    user_repo = UserRepository(db)
    user = user_repo.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        db.delete(user)
        db.commit()

        return {"detail": f"User with ID {user_id} deleted successfully."}

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete user due to integrity constraint: {str(e.orig)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while deleting user: {str(e)}"
        )


def update_user_last_visited_text(db: Session, user_id: int, text_id: int):
    try:
        user_repo = UserRepository(db)
        user_to_update = user_repo.get(user_id)
        user_to_update.last_visited_text_id = text_id

        user_repo.update(user_to_update)
        db.commit()

    except Exception:
        db.rollback()
        raise


def add_user_time(db: Session, user_id: int, seconds: int):
    """
    Adiciona tempo ao atributo study_time_in_seconds do usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário.
        seconds (int): Tempo em segundos a ser adicionado.

    Raises:
        HTTPException: Se o usuário não for encontrado.
    """
    user_repo = UserRepository(db)
    try:
        user_repo.add_study_time(user_id, seconds)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
