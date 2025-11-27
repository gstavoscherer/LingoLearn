from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user_id
from app.database.connection import get_db
from app.schemas.quiz import ReviewResponse, WordReviewRequest, QuizResponse
from app.services.quiz import get_quizzes, new_next_review

router = APIRouter(prefix="/quiz", tags=["quiz"])

@router.get("", response_model=QuizResponse)
def get_user_quizzes(user_id:int = Depends(get_current_user_id),db: Session = Depends(get_db)):
      return get_quizzes(user_id=user_id, db=db)


@router.post("", response_model=List[ReviewResponse])
def new_next_review_for_words(
    reviews: List[WordReviewRequest],
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return new_next_review(reviews=reviews, user_id=user_id, db=db)