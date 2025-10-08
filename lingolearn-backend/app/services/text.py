from repositories import TextRepository, PageRepository, TextWordRepository
from schemas.text import TextImport, TextResponse, TextListResponse
from core.utils import parse_text_into_pages, parse_text_into_words, get_text_total_words
import math
from utils.save_image import _save_upload_file
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile

def import_text(db: Session, text_data: TextImport, image: Optional[UploadFile]) -> TextResponse:
    try:
        text_repo = TextRepository(db)
        text_to_create = {
            "user_id": text_data.user_id,
            "title": text_data.title,
            "author": text_data.author,
            "language": text_data.language,
            "total_words": get_text_total_words(text_data.content),
        }
        new_text = text_repo.create(**text_to_create)
        db.flush()
        db.refresh(new_text)

        if image is not None:
            saved_path = _save_upload_file(
                upload=image,
                base_dir="uploads/text_covers",
                basename=f"text_{new_text.id}_cover",
            )
            text_repo.update(new_text, image_path=saved_path)
            new_text.image_path = saved_path

        page_repo = PageRepository(db)
        pages = parse_text_into_pages(text=text_data.content, words_per_page=300)
        for i, page in enumerate(pages, start=1):
            page_repo.create(text_id=new_text.id, number=i, content=page)

        word_repo = TextWordRepository(db)
        for word, count in parse_text_into_words(text_data.content):
            word_repo.create(text_id=new_text.id, normalized=word, appearance_count=count)

        db.commit()
        db.refresh(new_text)

        text_response = TextResponse(
            id=new_text.id,
            user_id=new_text.user_id,
            title=new_text.title,
            author=new_text.author,
            image_path=new_text.image_path or None,
            language=new_text.language,
            total_words=new_text.total_words,
            total_know_words=new_text.total_know_words,
        )
        return text_response

    except Exception:
        db.rollback()
        raise

def get_text_list(db: Session, user_id: int, top: int = 10, page: int = 1, query: str = '') -> TextListResponse:
    try:
        text_repo = TextRepository(db)
        filters = {
            "user_id": user_id
        }
        user_texts = text_repo.list_all(filters=filters)

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
                TextResponse(
                    id=text.id,
                    user_id=text.user_id,
                    title=text.title,
                    author=text.author,
                    image_path=text.image_path or None,
                    language=text.language,
                    total_know_words=text.total_know_words,
                    total_words=text.total_words

                )
                for text in paginated_texts
            ]
        )

        return text_list_response

    except Exception:
        db.rollback()
        raise
