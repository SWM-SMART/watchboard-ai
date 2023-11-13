from typing import List
from pydantic import BaseModel

class Document(BaseModel):
    key: str = ""
    dbType: str = ""
    keywords: List[str]
    documentId: int = 0