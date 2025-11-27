from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from sqlalchemy import select
from datetime import datetime

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    def get_user_streak(self, user_id: int) -> dict:
        stmt = select(User.streak, User.last_login).where(User.id == user_id)
        result = self.db.execute(stmt).first()

        if not result:
            return {"streak": 0, "last_login": None}

        streak, last_login = result
        streak = streak or 0

        return {"streak": streak, "last_login": last_login}

    def add_study_time(self, user_id: int, seconds: int):
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError(f"Usuário com ID {user_id} não encontrado.")

        current_date = datetime.now().date()

        if user.last_login is None or user.last_login.date() != current_date:
            # Novo dia, reseta o tempo de estudo
            user.study_time_in_seconds = seconds
            user.streak = 1 if user.last_login and (current_date - user.last_login.date()).days > 1 else user.streak + 1
        else:
            # Mesmo dia, soma o tempo
            if user.study_time_in_seconds is None:
                user.study_time_in_seconds = 0
            user.study_time_in_seconds += seconds

        # Atualiza o último login para o momento atual
        user.last_login = datetime.now()

        # Salva as alterações no banco de dados
        self.db.commit()

    def get_user_study_time_today(self, user_id: int) -> int:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError(f"Usuário com ID {user_id} não encontrado.")

        current_date = datetime.now().date()

        if user.last_login is None or user.last_login.date() != current_date:
            return 0

        return user.study_time_in_seconds or 0
