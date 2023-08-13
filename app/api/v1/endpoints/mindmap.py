from typing import Any

from fastapi import APIRouter
from app import schemas

router = APIRouter()

@router.post("/mindmap", response_model=schemas.MindMap)
def get_mind_map(text_data: schemas.Context) -> schemas.MindMap:
    
    test = schemas.MindMap(0, ["오늘", "밥", "마라탕"], {0: [1, 2]})
    return test