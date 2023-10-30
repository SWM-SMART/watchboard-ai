from fastapi import Depends
from app.controller.llm import LLMController
from langchain.schema.document import Document

from app.schemas.context import Keywords

class KeywordsController:
    prompt = "Question: 키워드들을 뽑아서 '(', ',', ')'로 정리해서 알려줘 \\nAnswer: ("
    def __init__(self, llm: LLMController = Depends(LLMController)):
        self.llm = llm

    def get_keywords(self, document: Document) -> Keywords:
        self.llm.set_document(document)
        answer = self.llm.request(self.prompt).content
        return Keywords(keywords=list(map(lambda word: word.strip()[1:-1], list(answer[1:-1].split(',')))))