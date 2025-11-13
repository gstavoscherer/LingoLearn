import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models import Base
from app.models.language import Language # Importe o modelo Language

# Criar engine e tabelas
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

print("Tabelas criadas.")

# Popular a tabela Language
with Session(engine) as session:
   # Verificar se já existem idiomas para evitar duplicação
   existing_languages = session.query(Language).count()

   if existing_languages == 0:
   # Criar os idiomas
      languages = [
         Language(name="Inglês", code="en"),
         Language(name="Português", code="pt"),
         Language(name="Espanhol", code="es")
         ]

      session.add_all(languages)
      session.commit()
      print("Idiomas padrão adicionados com sucesso!")
   else:
      print("Idiomas já existem na base de dados.")

      print("Processo concluído.")
