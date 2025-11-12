from re import U
from app.repositories.user import UserRepository
from sqlalchemy.orm import Session

from app.repositories.user_word import UserWordRepository
from app.schemas.dashboard import DashboardResponse

async def dashboard(db: Session, user_id: int) -> DashboardResponse: 

   user_words_repo = UserWordRepository(db)
   users_repo = UserRepository(db)

   total_user_known_words = user_words_repo.get_user_words_stats(user_id=user_id)
   total_user_known_words_last_week = user_words_repo.get_user_words_stats_last_week(user_id=user_id)
   user_streak = users_repo.get_user_streak(user_id=user_id)
   time_today = users_repo.get_user_study_time_today(user_id=user_id)

   return {
        "user_known_words": total_user_known_words.total,
        "user_known_words_last_week": total_user_known_words_last_week.total,
        "streak": user_streak["streak"],
        "last_login": user_streak["last_login"].isoformat() if user_streak["last_login"] else None,
        "study_time_today": time_today
    }
