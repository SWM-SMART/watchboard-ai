from fastapi import Depends
from app.controller.llm import LLMController
from langchain.schema.document import Document
from langchain.text_splitter import CharacterTextSplitter

from app.schemas.context import Keywords

class KeywordsController:
    def __init__(self, llm: LLMController):
        self.llm = llm

    def get_keywords(self, document: Document) -> Keywords:
        self.llm.set_document(document)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(document)
        prompt = f"#Context: {texts} \\n#Question: 한글 키워드들을 20개 이내로 뽑아서 '(', ',', ')'로 정리해서 알려줘 \\n#Answer: ("

        answer = self.llm.request_base(prompt)
        return Keywords(keywords=list(map(lambda word: word.strip(), list(answer[1:-1].split(',')))))