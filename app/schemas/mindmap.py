from pydantic import BaseModel

class MindMap(BaseModel):
    root: str = '0'
    keywords: list[str] = []
    graph: dict = {}