from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="RAG Q&A System")

app.include_router(api_router, prefix="/api")
