from fastapi import APIRouter
from app.api.v1.endpoints import mindmap

api_router = APIRouter()
api_router.include_router(mindmap.router)