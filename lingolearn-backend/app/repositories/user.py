from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from sqlalchemy import select
from datetime import datetime

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    def get_user_streak(self, user_id: int) -> dict:
        """
        Retorna o streak e o último login do usuário.

        Args:
            user_id (int): ID do usuário.

        Returns:
            dict: {"streak": int, "last_login": datetime | None}
        """
        stmt = select(User.streak, User.last_login).where(User.id == user_id)
        result = self.db.execute(stmt).first()

        if not result:
            print(f"⚠️ [STREAK] Usuário {user_id} não encontrado.")
            return {"streak": 0, "last_login": None}

        streak, last_login = result
        streak = streak or 0

        print(f"🔥 [STREAK] user_id={user_id}, streak={streak}, last_login={last_login}")
        return {"streak": streak, "last_login": last_login}

    def add_study_time(self, user_id: int, seconds: int):
        """
        Adiciona tempo ao atributo study_time_in_seconds do usuário.
        Reseta o tempo se for um novo dia, ou soma ao tempo existente se for o mesmo dia.

        Args:
            user_id (int): ID do usuário.
            seconds (int): Tempo em segundos a ser adicionado.
        """
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
        """
        Retorna o tempo de estudo do usuário no dia atual.

        Args:
            user_id (int): ID do usuário.

        Returns:
            int: Tempo de estudo em segundos no dia atual.
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError(f"Usuário com ID {user_id} não encontrado.")

        current_date = datetime.now().date()

        if user.last_login is None or user.last_login.date() != current_date:
            return 0

        return user.study_time_in_seconds or 0
