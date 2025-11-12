from fastapi import FastAPI, Request, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import auth, users, texts, languages, user_words, pages,words, text_words, translate, dashboard
from app.database.connection import engine, Base
from app.core.exceptions import AppError

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware to handle X-Forwarded-Proto
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        forwarded_proto = request.headers.get("X-Forwarded-Proto")
        if forwarded_proto:
            request.scope["scheme"] = forwarded_proto
        response = await call_next(request)
        return response

app.add_middleware(ProxyHeadersMiddleware)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://lingolearn.gustavoscherer.com",
    "http://lingolearn.gustavoscherer.com",
]

@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    print(exc.message)
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
            }
        }
    )
app.mount("/uploads/text_covers", StaticFiles(directory="uploads/text_covers"), name="uploads")
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
app.include_router(languages.router)
app.include_router(pages.router)
app.include_router(words.router)
app.include_router(text_words.router)
app.include_router(user_words.router)
app.include_router(translate.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {"message": "API de Usuários"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=5000,
        reload=True
    )
