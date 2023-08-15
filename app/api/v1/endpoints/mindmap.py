from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException, Header
from app import schemas
from app.api.deps import get_mindmap_model

import jwt

router = APIRouter()
key = "qwrkljvpoqdmrqlwkjfvp12ti1ej1j213klg1k4j43l1k13lkjjk2mcp27ax80cnp1"

@router.post("/mindmap", response_model=schemas.MindMap)
def get_mind_map(
    Authorization: Optional[str] = Header(None),
    text_data: schemas.Context = schemas.Context(), 
    mindmap_controller = Depends(get_mindmap_model)
    ) -> schemas.MindMap:
    auth = Authorization.split(' ')
    if auth[0] == 'Bearer':
        payload = jwt.decode(auth[1], key, algorithms=["HS512"])
        if payload['issuer'] == 'wb':
            return mindmap_controller.transform(text_data)
    raise HTTPException(status_code=401, detail="You're not my user")