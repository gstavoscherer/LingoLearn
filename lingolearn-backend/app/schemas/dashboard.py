from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DashboardResponse(BaseModel):
    user_known_words: int
    user_known_words_last_week: int
    streak: int
    last_login: Optional[str] = None
    study_time_today: int
    words_to_review: int

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }