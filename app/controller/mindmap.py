from fastapi import Depends
from app.controller.llm import LLMController
from langchain.schema.document import Document
from langchain.text_splitter import CharacterTextSplitter

from app.schemas.mindmap import MindMap
from app.schemas.context import Keywords

import re

from typing import List

class MindMapController:
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
        mindmap.keywords = []
        keyword2index = {}
        lines = markdown.split('\n')

        for index, line in enumerate(lines):
            if len(line.split('- ')) == 1: continue
            word = '- '.join(line.split('- ')[1:])
            keyword2index[word] = index-1
            mindmap.keywords.append(word)
        print(mindmap.keywords)
        print(keyword2index)

        current = 0
        stack = []
        for line in lines:
            if len(line.split('- ')) == 1: continue
            sep = line.split('- ')[0]
            word = '- '.join(line.split('- ')[1:])
            if word in mindmap.keywords:
                sep = len(sep)
                mindmap.graph[str(keyword2index[word])] = []

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
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(document)

        prompt = f"#Context: {texts} \\nQuestion: 문맥 내에서 {keywords}들의 계층 구조를 MarkDown의 '-'로 알려줘 \nAnswer: -"    
        answer = self.llm.request_base(prompt)
        print(answer)
        answer = self.delete_stopwords(answer)
        return self.parse_html(answer, keywords)