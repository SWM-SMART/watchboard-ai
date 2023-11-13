from pydantic import BaseModel

class DatabaseInfo(BaseModel):
    key: str = ""
    dbType: str = ""