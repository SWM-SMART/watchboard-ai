from fastapi import Depends
from app.controller.llm import LLMController
from langchain.schema.document import Document

from app.schemas.mindmap import MindMap
from app.schemas.context import Keywords

import re

from typing import List

class MindMapController:
    prompt = "Question: 문맥 내에서 %s들의 계층 구조를 MarkDown의 '-'로 알려줘 \nAnswer: -"
    def __init__(self, llm: LLMController = Depends(LLMController)):
        self.llm = llm

    def delete_stopwords(self, html: str) -> str:
        with open('app/static/stopwords.txt') as f:
            stopwords = f.read().split('\n')
            for stopword in stopwords:
                html.replace(stopword, '')
        return html

    def parse_html(self, markdown: str, keywords: List[str]) -> MindMap:
        mindmap = MindMap()
        mindmap.keywords = keywords
        keyword2index = {v: i for i, v in enumerate(keywords)}

        current = 0
        stack = []
        lines = markdown.split('\n')
        for line in lines:
            sep = line.split('- ')[0]
            word = line.split('- ')[-1]
            if word in keywords:
                sep = len(sep)
                mindmap.graph[str(keyword2index[word])] = []
                print(stack)

                if sep == 0:
                    mindmap.root = sep
        
                if current == sep:
                    if len(stack) != 0: stack.pop()
                    if len(stack) != 0: mindmap.graph[str(stack[-1])].append(keyword2index[word])
                    stack.append(keyword2index[word])
                elif current < sep:
                    mindmap.graph[str(stack[-1])].append(keyword2index[word])
                    stack.append(keyword2index[word])
                else:
                    stack.pop()
                    if len(stack) != 0: mindmap.graph[str(stack[-1])].append(keyword2index[word])
                current = sep
        return mindmap

    def get_mindmap(self, document: Document, keywords: List[str]) -> MindMap:
        self.llm.set_document(document)
        answer = self.llm.request(self.prompt % keywords).content
        print(answer)
        answer = self.delete_stopwords(answer)
        return self.parse_html(answer, keywords)