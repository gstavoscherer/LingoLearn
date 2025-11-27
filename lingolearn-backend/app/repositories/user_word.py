from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from app.models import UserWord, Word
from app.repositories.base_repository import BaseRepository
from app.schemas.user_word import WordStats

class UserWordRepository(BaseRepository[UserWord]):
    def __init__(self, db: Session):
        super().__init__(UserWord, db)

    def get_by_user_and_word(self, user_id: int, word_id: int):
        stmt = select(self.model).where(
            self.model.user_id == user_id,
            self.model.word_id == word_id
        )
        return self.db.scalars(stmt).first()

    def create(self, **kwargs):
        user_id = kwargs.get("user_id")
        word_id = kwargs.get("word_id")

        existing = self.get_by_user_and_word(user_id, word_id)
        if existing:
            for key, value in kwargs.items():
                setattr(existing, key, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing

        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_user_word(
        self, 
        user_id: int, 
        word_id: int, 
        **kwargs
    ) -> Optional[UserWord]:
        """
        Atualiza uma UserWord específica, modificando apenas os campos passados.
        
        Args:
            user_id: ID do usuário
            word_id: ID da palavra
            **kwargs: Campos para atualizar (apenas os campos passados serão modificados)
            
        Returns:
            UserWord atualizada ou None se não encontrada
        """
        user_word = self.get_by_user_and_word(user_id, word_id)
        
        if not user_word:
            return None
        
        # Atualiza apenas os campos que foram passados
        for key, value in kwargs.items():
            if hasattr(user_word, key):
                setattr(user_word, key, value)
        
        self.db.commit()
        self.db.refresh(user_word)
        return user_word

    # Método alternativo mais explícito
    def update_user_word_explicit(
        self, 
        user_id: int, 
        word_id: int, 
        easiness_factor: Optional[float] = None,
        translation: Optional[str] = None,
        context: Optional[str] = None,
        context_translation: Optional[str] = None,
        last_review: Optional[datetime] = None,
        next_review: Optional[datetime] = None
    ) -> Optional[UserWord]:
        """
        Versão explícita do update que aceita apenas os campos específicos da UserWord.
        """
        user_word = self.get_by_user_and_word(user_id, word_id)
        
        if not user_word:
            return None
        
        # Atualiza apenas os campos que não são None
        update_fields = {
            'easiness_factor': easiness_factor,
            'translation': translation,
            'context': context,
            'context_translation': context_translation,
            'last_review': last_review,
            'next_review': next_review
        }
        
        for field, value in update_fields.items():
            if value is not None:
                setattr(user_word, field, value)
        
        self.db.commit()
        self.db.refresh(user_word)
        return user_word

    def get_user_words_by_language(
        self, 
        user_id: int, 
        language_id: int,
        *,
        skip: int = 0,
        limit: int = 100,
        load_relationships: Optional[List[str]] = None
    ) -> List[UserWord]:
        """
        Busca todas as palavras de um usuário por language_id.
        
        Args:
            user_id: ID do usuário
            language_id: ID do idioma (ex: 1 = português)
            skip: Número de registros para pular (paginação)
            limit: Número máximo de registros a retornar
            load_relationships: Lista de relacionamentos para carregar
            
        Returns:
            Lista de UserWord do usuário no idioma especificado
        """
        # Join com a tabela Word para filtrar por language_id
        stmt = (
            select(UserWord)
            .join(UserWord.word)
            .where(
                UserWord.user_id == user_id,
                Word.language_id == language_id
            )
            .offset(skip)
            .limit(limit)
        )
        
        # Carrega relacionamentos se especificados
        if load_relationships:
            for rel in load_relationships:
                stmt = stmt.options(joinedload(getattr(UserWord, rel)))
        
        return list(self.db.scalars(stmt).all())
    
    def get_user_words_paginated(
        self, 
        user_id: int, 
        query: str = None,  # Novo filtro
        language_id: int = None,
        status: str = None,
        limit: int = 20, 
        offset: int = 0
    ) -> tuple[List[UserWord], int]:
        query_obj = self.db.query(UserWord).join(Word).filter(
            UserWord.user_id == user_id
        )
        
        # Filtrar por language_id apenas se fornecido
        if language_id is not None:
            query_obj = query_obj.filter(Word.language_id == language_id)
        
        # Aplicar filtro de query (substring em word ou translation)
        if query:
            # Busca case-insensitive por substring no word ou translation
            search_pattern = f"%{query}%"
            query_obj = query_obj.filter(
                or_(
                    Word.word.ilike(search_pattern),
                    UserWord.translation.ilike(search_pattern)
                )
            )
        
        # Aplicar filtro de status baseado no easiness_factor
        if status:
            if status == 'new':
                query_obj = query_obj.filter(UserWord.easiness_factor < 1.6)
            elif status == 'learning':
                query_obj = query_obj.filter(
                    UserWord.easiness_factor >= 1.6, 
                    UserWord.easiness_factor < 2.0
                )
            elif status == 'known':
                query_obj = query_obj.filter(UserWord.easiness_factor >= 2.0)
        
        # Contar total (antes da paginação)
        total_count = query_obj.count()
        
        # Aplicar paginação
        results = query_obj.offset(offset).limit(limit).all()
        
        return results, total_count
    
    def get_user_words_stats(
        self, 
        user_id: int, 
        query: str = None,  # Novo filtro
        language_id: int = None
    ) -> WordStats:
        # Query base
        query_obj = self.db.query(UserWord).join(Word).filter(
            UserWord.user_id == user_id
        )
        
        # Filtrar por language_id apenas se fornecido
        if language_id is not None:
            query_obj = query_obj.filter(Word.language_id == language_id)
        
        # Aplicar filtro de query se fornecido
        if query:
            search_pattern = f"%{query}%"
            query_obj = query_obj.filter(
                or_(
                    Word.word.ilike(search_pattern),
                    UserWord.translation.ilike(search_pattern)
                )
            )
        
        # Total geral
        total = query_obj.count()
        
        # Por status
        known = query_obj.filter(UserWord.easiness_factor >= 2.0).count()
        learning = query_obj.filter(
            UserWord.easiness_factor >= 1.6,
            UserWord.easiness_factor < 2.0
        ).count()
        new = query_obj.filter(UserWord.easiness_factor < 1.6).count()
        
        return WordStats(
            total=total,
            known=known,
            learning=learning,
            new=new
        )
    
    def get_user_words_stats_last_week(
        self, 
        user_id: int, 
        query: str = None,  
        language_id: int = None
    ) -> WordStats:
        last_week_date = datetime.now() - timedelta(weeks=1)
    
        query_obj = self.db.query(UserWord).join(Word).filter(
            UserWord.user_id == user_id,
            UserWord.created_at >= last_week_date
        )
        
        # Filtrar por language_id apenas se fornecido
        if language_id is not None:
            query_obj = query_obj.filter(Word.language_id == language_id)
        
        # Aplicar filtro de query se fornecido
        if query:
            search_pattern = f"%{query}%"
            query_obj = query_obj.filter(
                or_(
                    Word.word.ilike(search_pattern),
                    UserWord.translation.ilike(search_pattern)

                )
            )
        # Total geral
        total = query_obj.count()
        
        # Por status
        known = query_obj.filter(UserWord.easiness_factor >= 2.0).count()
        learning = query_obj.filter(
            UserWord.easiness_factor >= 1.6,
            UserWord.easiness_factor < 2.0
        ).count()
        new = query_obj.filter(UserWord.easiness_factor < 1.6).count()
        
        return WordStats(
            total=total,
            known=known,
            learning=learning,
            new=new
        )
    
    def get_user_words_to_review(self, user_id: int, top: int = 5):
        now = datetime.now()

        stmt = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
                or_(
                    self.model.next_review == None,         
                    self.model.next_review <= now          
                )
            )
            .order_by(
                self.model.last_review.is_(None).desc(),   
                self.model.last_review.desc()            
            )
            .limit(top)
        )

        return self.db.execute(stmt).scalars().all()
    
    def get_all_user_words(self, user_id:int):
        stmt = select(self.model).where(
            self.model.user_id == user_id
        ) 
        return self.db.execute(stmt).scalars(stmt).all()