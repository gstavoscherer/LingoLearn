
from datetime import datetime, timedelta
import random
from math import ceil

from requests import Session
from app.repositories.user_word import UserWordRepository
from app.repositories.word import WordRepository
from sqlalchemy.orm import Session
from app.repositories.user_word import UserWordRepository
from app.repositories.word import WordRepository
from app.schemas.quiz import ReviewResponse, QuizResponse, QuizQuestion
from app.schemas.word import WordResponse

def get_quizzes(user_id: int, db: Session) -> QuizResponse:
    number_of_options = 4
    user_word_repo = UserWordRepository(db=db)
    word_repo = WordRepository(db=db)

    user_words = user_word_repo.get_user_words_to_review(user_id)  
    all_user_words = user_word_repo.get_all_user_words(user_id) 

    if len(user_words) < 5:
        random_words = user_words
    else:
        random_words = random.sample(user_words, 5)

    quiz = []

    for user_word in random_words:
        correct_answer_id = user_word.word_id
        correct_answer = word_repo.get_word_by_id(correct_answer_id)

        if not correct_answer:
            continue 

        context_with_blank = user_word.context.replace(correct_answer.word, "_____", 1)

        wrong_options_needed = number_of_options - 1
        
        other_user_words = [w for w in all_user_words if w.word_id != correct_answer_id]
        if len(other_user_words) >= wrong_options_needed:
            other_user_words = random.sample(other_user_words, wrong_options_needed)
        else:
            other_user_words = other_user_words
        
        other_answers = [word_repo.get_word_by_id(w.word_id) for w in other_user_words]
        other_answers = [answer for answer in other_answers if answer is not None]
        
        if len(other_answers) < wrong_options_needed:
            continue
        
        options = [correct_answer] + other_answers
        random.shuffle(options)

        options_response = [
            WordResponse(id=w.id, word=w.word, language_id=w.language_id)
            for w in options
        ]

        question = QuizQuestion(
            question=context_with_blank,
            options=options_response,
            correct_answer_id=correct_answer_id
        )

        quiz.append(question)

    return QuizResponse(quiz=quiz)


def calculate_new_values(EF: float, q: int, last_review: datetime, next_review: datetime):
    EF_new = EF - 0.8 + 0.28 * q - 0.02 * (q ** 2)
    EF_new = max(EF_new, 1.3)
    
    interval = max((next_review - last_review).days, 1)
    interval_new = ceil(interval * EF_new)
    
    next_review = last_review + timedelta(days=interval_new)
    
    return EF_new, next_review

def new_next_review(reviews, user_id: int, db: Session):
    user_word_repo = UserWordRepository(db=db)
    results = []
    
    for review in reviews:
        word_id = review.word_id
        quality = review.response_quality
        
        # Buscar a UserWord para a palavra do usuário
        user_word = user_word_repo.get_by_user_and_word(user_id=user_id, word_id=word_id)
        
        if not user_word:
            continue
        
        # Usar a data atual como last_review se não existir
        last_review = user_word.last_review or datetime.now()
        next_review = user_word.next_review or datetime.now()
        EF = user_word.easiness_factor  # Corrigido para easiness_factor
        
        # Calcular os novos valores com base na qualidade da resposta
        EF_new, next_review = calculate_new_values(
            EF=EF,
            q=quality,
            last_review=last_review,
            next_review=next_review
        )
        
        # Atualizar a UserWord com os novos valores
        # Note que só atualizamos os campos que existem na model
        user_word_repo.update_user_word(
            word_id=word_id,
            user_id=user_id,
            easiness_factor=EF_new,  # Corrigido para easiness_factor
            last_review=datetime.now(),  # Atualizar para a data atual
            next_review=next_review
        )
        
        results.append(ReviewResponse(
            word_id=word_id, 
            next_review=next_review.strftime("%Y-%m-%d %H:%M:%S")
        ))
    
    return results