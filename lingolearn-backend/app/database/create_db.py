import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from app.core.config import settings
from app.models import Base

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
print("Tabelas criadas.")