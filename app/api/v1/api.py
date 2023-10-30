from fastapi import APIRouter
from app.api.v1.endpoints import mindmap
from app.api.v1.endpoints import keywords
from app.api.v1.endpoints import question
from app.api.v1.endpoints import summary

api_router = APIRouter()
api_router.include_router(mindmap.router)
api_router.include_router(keywords.router)
api_router.include_router(question.router)
api_router.include_router(summary.router)