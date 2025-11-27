
from pydantic import BaseModel
from app.schemas.word import WordResponse

class WordReviewRequest(BaseModel):
    word_id: int
    response_quality: int 

class ReviewResponse(BaseModel):
    word_id: int
    next_review: str

class QuizQuestion(BaseModel):
    question: str
    options: list[WordResponse]
    correct_answer_id: int

class QuizResponse(BaseModel):
    quiz: list[QuizQuestion]

