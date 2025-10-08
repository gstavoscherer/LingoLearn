from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.user import register_user, update_user
from schemas.user import UserCreate, UserResponse, UserUpdate
from database.connection import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def register_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db)
):  
    return register_user(db, user)

@router.put("/{id}", response_model=UserResponse, status_code=200)
def update_user_endpoint(
    id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    return update_user(db, user_id=id, user_data=user)
    