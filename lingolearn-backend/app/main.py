from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, texts
from starlette.staticfiles import StaticFiles
from database.connection import engine, Base
from core.exceptions import *
import os
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
            }
        }
    )
# Caminho do diretório de uploads
UPLOAD_DIR = "uploads/text_covers"

# 🔧 Fallback: cria o diretório se não existir
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Monta o diretório estático
app.mount("/uploads/text_covers", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(texts.router)

@app.get("/")
def home():
    return {"message": "API de Usuários"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=5000,
        reload=True
    )