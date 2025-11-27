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
    user_word_repo = UserWordRepository(db)
    text_repo = TextRepository(db)
    page_repo = PageRepository(db)
    word_repo = WordRepository(db)
    text_word_repo = TextWordRepository(db)

    try:
        print("=== DEBUG IMPORT_TEXT ===")
        print(f"📝 Iniciando importação do texto: {text_data.title}")
        print(f"👤 User ID: {text_data.user_id}")
        print(f"🌐 Language ID: {text_data.language_id}")
        print(f"📄 Tamanho do conteúdo: {len(text_data.content)} caracteres")
        print(f"🖼️ Imagem fornecida: {image is not None}")

        # 1. Calcular palavras conhecidas
        print("\n🔍 Buscando palavras conhecidas do usuário...")
        user_known_words = user_word_repo.get_user_words_by_language(
            user_id=text_data.user_id,
            language_id=text_data.language_id
        )
        print(f"✅ Palavras conhecidas encontradas: {len(user_known_words)}")

        print("\n📖 Parseando texto em palavras...")
        parsed_words = parse_text_into_words(text_data.content)
        words_from_text = {word for word, count in parsed_words}
        print(f"📊 Palavras únicas no texto: {len(words_from_text)}")
        print(f"📈 Total de ocorrências: {sum(count for word, count in parsed_words)}")
        
        # Mostrar algumas palavras do texto
        sample_words = list(words_from_text)[:10]
        print(f"🔤 Amostra de palavras: {sample_words}")

        known_words_set = {user_word.word.word for user_word in user_known_words}
        print(f"📚 Palavras conhecidas do usuário: {len(known_words_set)}")
        
        known_words_in_text = words_from_text.intersection(known_words_set)
        total_known_words = len(known_words_in_text)
        print(f"🎯 Palavras conhecidas NO TEXTO: {total_known_words}")
        print(f"📊 Porcentagem conhecida: {(total_known_words/len(words_from_text))*100:.1f}%")

        print("\n📄 Dividindo texto em páginas...")
        pages = parse_text_into_pages(text=text_data.content, words_per_page=300)
        print(f"📖 Total de páginas: {len(pages)}")
        print(f"📝 Caracteres por página: {[len(page) for page in pages[:3]]}...")

        # 2. Criar texto
        print("\n💾 Criando registro do texto...")
        text_to_create = {
            "user_id": text_data.user_id,
            "title": text_data.title,
            "author": text_data.author,
            "language_id": text_data.language_id,
            "total_words": get_text_total_words(text_data.content),
            "total_known_words": total_known_words,
            "total_pages": len(pages)
        }
        print(f"📋 Dados do texto: {text_to_create}")
        
        new_text = text_repo.create(**text_to_create)
        db.flush()
        print(f"✅ Texto criado com ID: {new_text.id}")

        # 3. Salvar imagem se existir
        if image:
            print(f"\n🖼️ Salvando imagem...")
            saved_path = save_upload_file(
                upload=image,
                base_dir="uploads/text_covers",
                basename=f"text_{new_text.id}_cover",
            )
            text_repo.update(new_text, image_path=saved_path)
            print(f"✅ Imagem salva em: {saved_path}")

        # 4. Criar páginas
        print(f"\n📄 Criando {len(pages)} páginas...")
        for i, page in enumerate(pages, start=1):
            page_repo.create(text_id=new_text.id, number=i, content=page)
        print("✅ Páginas criadas com sucesso")

        # 5. Processar palavras
        print(f"\n🔤 Processando {len(parsed_words)} palavras...")
        words_to_process = [(word_str, count) for word_str, count in parsed_words]
        print(f"📊 Palavras únicas para processar: {len(words_to_process)}")

        # Buscar todas as palavras existentes de uma vez
        print("🔍 Buscando palavras existentes no banco...")
        word_strings = [word for word, count in words_to_process]
        existing_words = word_repo.get_words_by_list(
            word_strings,
            text_data.language_id
        )
        print(f"✅ Palavras existentes encontradas: {len(existing_words)}")

        # Criar dicionário para acesso rápido
        existing_words_dict = {word.word: word for word in existing_words}
        print(f"📚 Dicionário de palavras existentes criado")

        # Identificar palavras que precisam ser criadas
        words_to_create = [
            word for word, count in words_to_process
            if word not in existing_words_dict
        ]
        print(f"🆕 Novas palavras a criar: {len(words_to_create)}")
        if words_to_create:
            print(f"📝 Amostra de novas palavras: {words_to_create[:10]}")

        # Criar todas as palavras novas de uma vez (INSERT BATCH)
        if words_to_create:
            print("💾 Criando palavras novas em lote...")
            new_words = word_repo.bulk_create(
                words_to_create,
                text_data.language_id
            )
            print(f"✅ {len(new_words)} novas palavras criadas")
            # Atualizar o dicionário com as novas palavras
            for word in new_words:
                existing_words_dict[word.word] = word

        # Criar todos os TextWords de uma vez (INSERT BATCH)
        print("\n🔗 Criando relações Text-Word...")
        aggregated = defaultdict(int)
        for word, count in words_to_process:
            aggregated[word] += count

        print(f"📊 Agregado de palavras: {len(aggregated)} entradas únicas")
        
        # Cria apenas um registro por word_id
        text_words_data = [
            {
                'text_id': new_text.id,
                'word_id': existing_words_dict[word].id,
                'quantity': aggregated[word]
            }
            for word in aggregated
        ]

        print(f"💾 Salvando {len(text_words_data)} relações Text-Word...")
        text_word_repo.bulk_create(text_words_data)
        print("✅ Relações Text-Word criadas com sucesso")

        db.commit()
        db.refresh(new_text)
        print("\n🎉 Importação concluída com sucesso!")
        print(f"📊 Resumo final:")
        print(f"   - Texto ID: {new_text.id}")
        print(f"   - Total palavras: {new_text.total_words}")
        print(f"   - Palavras conhecidas: {new_text.total_known_words}")
        print(f"   - Páginas: {new_text.total_pages}")

        # 6. Retornar resposta
        return TextResponse.model_validate(new_text)
        
    except Exception as e:
        print(f"\n❌ ERRO na importação: {str(e)}")
        print(f"🔍 Tipo do erro: {type(e).__name__}")
        import traceback
        print(f"📋 Stack trace: {traceback.format_exc()}")
        db.rollback()
        print("🔄 Rollback executado")
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
