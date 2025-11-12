from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user_id
from app.database.connection import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import (
    register_user,
    update_user,
    get_user_by_id,
    list_users,
    delete_user,
    add_user_time,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=201)
def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id=user_id, user_data=user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[UserResponse])
def list_users_endpoint(db: Session = Depends(get_db)):
    return list_users(db)


@router.delete("/{user_id}", status_code=204)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)

@router.post("/add-user-time", status_code=200)
def add_user_time_endpoint(seconds: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    add_user_time(db, user_id, seconds)
    return {"message": f"Added {seconds} seconds to user {user_id}."}
