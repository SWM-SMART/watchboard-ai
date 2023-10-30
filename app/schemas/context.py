from typing import List
from pydantic import BaseModel

class Keywords(BaseModel):
    keywords: List[str] = []

class Text(BaseModel):
    text: str

class Context(BaseModel):
    keyword: str = ""
    summary: str = ""
