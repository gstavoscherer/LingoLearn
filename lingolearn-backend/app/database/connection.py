from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

if __name__=="__main__":
    from app.models import *  
    Base.metadata.create_all(bind=engine)