from typing import List
from pydantic import BaseModel

from app.schemas.context import Keywords

class MindMap(BaseModel):
    root: str = ""
    keywords: Keywords = []
    graph: dict = {}