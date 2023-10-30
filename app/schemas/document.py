from typing import List
from pydantic import BaseModel

from app.schemas.database import DatabaseInfo
from app.schemas.context import Keywords

class Document(BaseModel):
    dbInfo: DatabaseInfo
    keywords: List[str]
    documentId: int = 0