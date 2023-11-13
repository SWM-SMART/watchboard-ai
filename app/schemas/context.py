from typing import List
from pydantic import BaseModel

class Keywords(BaseModel):
    keywords: List[str] = []

class Text(BaseModel):
    summary: str

class Context(BaseModel):
    keyword: str = ""
    summary: str = ""

class Audio(BaseModel):
    key: str

class Segment(BaseModel):
    start: int
    end: int
    text: str

class SpeechText(BaseModel):
    segments: List[Segment]
    text: str