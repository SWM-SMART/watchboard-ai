from pydantic import BaseModel

class MindMap(BaseModel):
    root: int
    keywords: list[str]
    graph: dict