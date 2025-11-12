from typing import Optional
import math
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import UploadFile
from collections import defaultdict
from app.repositories.user_word import UserWordRepository
from app.repositories.text import TextRepository
from app.repositories.page import PageRepository
from app.repositories.text_word import TextWordRepository
from app.repositories.word import WordRepository
from app.schemas.text import TextImport, TextResponse, TextListResponse, TextUpdate, TextPageResponse
from app.core.utils import parse_text_into_pages, parse_text_into_words, get_text_total_words, save_upload_file
from app.core.exceptions import ResourceNotFoundException


def import_text(db: Session, text_data: TextImport, image: Optional[UploadFile]) -> TextResponse:
    # Repositórios
    user_word_repo = UserWordRepository(db)
    text_repo = TextRepository(db)
    page_repo = PageRepository(db)
    word_repo = WordRepository(db)
    text_word_repo = TextWordRepository(db)

    try:
        # 1. Calcular palavras conhecidas
        user_known_words = user_word_repo.get_user_words_by_language(
            user_id=text_data.user_id,
            language_id=text_data.language_id
        )
        parsed_words = parse_text_into_words(text_data.content)
        words_from_text = {word for word, count in parsed_words}
        known_words_set = {user_word.word.word for user_word in user_known_words}
        known_words_in_text = words_from_text.intersection(known_words_set)
        total_known_words = len(known_words_in_text)

        pages = parse_text_into_pages(text=text_data.content, words_per_page=300)

        # 2. Criar texto
        text_to_create = {
            "user_id": text_data.user_id,
            "title": text_data.title,
            "author": text_data.author,
            "language_id": text_data.language_id,
            "total_words": get_text_total_words(text_data.content),
            "total_known_words": total_known_words,
            "total_pages": len(pages)
        }
        new_text = text_repo.create(**text_to_create)
        db.flush()

        # 3. Salvar imagem se existir
        if image:
            saved_path = save_upload_file(
                upload=image,
                base_dir="uploads/text_covers",
                basename=f"text_{new_text.id}_cover",
            )
            text_repo.update(new_text, image_path=saved_path)

        # 4. Criar páginas
        for i, page in enumerate(pages, start=1):
            page_repo.create(text_id=new_text.id, number=i, content=page)

        # 5. Processar palavras - OTIMIZADO
        words_to_process = [(word_str, count) for word_str, count in parsed_words]

        # Buscar todas as palavras existentes de uma vez
        existing_words = word_repo.get_words_by_list(
            [word for word, count in words_to_process],
            text_data.language_id
        )

        # Criar dicionário para acesso rápido
        existing_words_dict = {word.word: word for word in existing_words}

        # Identificar palavras que precisam ser criadas
        words_to_create = [
            word for word, count in words_to_process
            if word not in existing_words_dict
        ]

        # Criar todas as palavras novas de uma vez (INSERT BATCH)
        if words_to_create:
            new_words = word_repo.bulk_create(
                words_to_create,
                text_data.language_id
            )
            # Atualizar o dicionário com as novas palavras
            for word in new_words:
                existing_words_dict[word.word] = word

        # Criar todos os TextWords de uma vez (INSERT BATCH)
        aggregated = defaultdict(int)
        for word, count in words_to_process:
            aggregated[word] += count

        # Cria apenas um registro por word_id
        text_words_data = [
            {
                'text_id': new_text.id,
                'word_id': existing_words_dict[word].id,
                'quantity': aggregated[word]
            }
            for word in aggregated
]

        text_word_repo.bulk_create(text_words_data)

        db.commit()
        db.refresh(new_text)

        # 6. Retornar resposta
        return TextResponse.model_validate(new_text)
    except:
        db.rollback()
        raise

def get_text_by_id(db: Session, text_id: int) -> TextResponse:
    text_repo = TextRepository(db)
    text = text_repo.get(text_id)
    return TextResponse.model_validate(text)

def get_text_list(db: Session, user_id: int, language_id: Optional[int], order_by: str, top: int = 5, page: int = 1, query: str = '') -> TextListResponse:
    try:
        text_repo = TextRepository(db)
        filters = {
            "user_id": user_id,
        }

        if language_id:
            filters["language_id"] = language_id

        if order_by == 'ascending':
            order_by = 'created_at ASC'
        else:
            order_by = 'created_at DESC'

        user_texts = text_repo.list_all(filters=filters, order_by=order_by)

        if query:
            filtered_texts = [
                text for text in user_texts
                if query.lower() in text.author.lower() or query.lower() in text.title.lower()
            ]
        else:
            filtered_texts = user_texts

        total = len(filtered_texts)
        start_index = (page - 1) * top
        end_index = start_index + top
        paginated_texts = filtered_texts[start_index:end_index]

        text_list_response = TextListResponse(
            page=page,
            total=total,
            total_pages=math.ceil(total / top) if top > 0 else 1,
            per_page=top,
            texts=[
                TextResponse.model_validate(text)
                for text in paginated_texts
            ]
        )

        return text_list_response

    except Exception:
        db.rollback()
        raise

def update_text(db: Session, data: TextUpdate, text_id: int) -> TextResponse:
    try:
        text_repo = TextRepository(db)

        text_to_update = text_repo.get(text_id)

        update_data = {k: v for k, v in vars(data).items() if v is not None}

        for field, value in update_data.items():
            if hasattr(text_to_update, field):
                setattr(text_to_update, field, value)

        db.commit()
        db.refresh(text_to_update)

        response = TextResponse.model_validate(text_to_update)
        return response
    except Exception:
        db.rollback()
        raise

def delete_text(db: Session, text_id: int):
    try:
        text_repo = TextRepository(db)
        text = text_repo.get(text_id)

        if not text:
            raise ResourceNotFoundException()

        text_repo.delete(text)
        db.commit()

    except Exception:
        db.rollback()
        raise

def text_page(db: Session, text_id: int, page_number: int) -> TextPageResponse:
    page_repo = PageRepository(db)
    page = page_repo.get_by(text_id=text_id, number=page_number)

    text_repo = TextRepository(db)
    text = text_repo.get(text_id)

    response = TextPageResponse(
        text=text,
        page=page
    )

    return TextPageResponse.model_validate(response)

def update_last_page(db: Session, text_id: int, page_number: int) -> None:
    try:
        text_repo = TextRepository(db)
        text_to_update = text_repo.get(text_id)
        text_to_update.last_visited_page = page_number

        text_repo.update(text_to_update)
        db.commit()

    except Exception:
        db.rollback()
        raise
