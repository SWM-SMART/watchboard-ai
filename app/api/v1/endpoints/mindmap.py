from typing import Any

from fastapi import APIRouter, Depends
from app import schemas
from app.api.deps import get_mindmap_model

router = APIRouter()

@router.post("/mindmap", response_model=schemas.MindMap)
def get_mind_map(text_data: schemas.Context, mindmap_controller = Depends(get_mindmap_model)) -> schemas.MindMap:
    return mindmap_controller.transform(text_data)