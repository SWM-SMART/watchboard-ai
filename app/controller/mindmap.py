from fastapi import Depends
from app.controller.llm import LLMController
from langchain.schema.document import Document

from app.schemas.mindmap import MindMap
from app.schemas.context import Keywords

from bs4 import BeautifulSoup

from typing import List

class MindMapController:
    prompt = "Question: 문맥 내에서 %s들의 계층 구조를 html 문법으로 알려줘 \nAnswer: <html>"
    def __init__(self, llm: LLMController = Depends(LLMController)):
        self.llm = llm

    def delete_stopwords(self, html: str) -> str:
        with open('app/static/stopwords.txt') as f:
            stopwords = f.read().split('\n')
            for stopword in stopwords:
                html.replace(stopword, '')
        return html

    def parse_html(self, html: str, keywords: List[str]) -> MindMap:
        mindmap = MindMap()
        mindmap.keywords = keywords
        keyword2index = {w: i for i, w in enumerate(keywords)}

        soup = BeautifulSoup(html, 'html.parser')
        prettified_html = soup.prettify()
        prettified_html = list(map(lambda x: x.strip(), prettified_html.split('\n')))
        prettified_html = [html for html in prettified_html if (html in keywords) or (html in ['<ul>', '</ul>'])]

        stack = []
        for index, word in enumerate(prettified_html):
            if word == '</ul>': stack.pop(len(stack)-1)
            if word in keywords:
                if len(stack) == 0:
                    stack.append(word)
                    mindmap.root = keyword2index[stack[0]]
                else:
                    if prettified_html[index-1] != '<ul>': stack.pop(len(stack)-1)
                    key = str(keyword2index[mindmap.root]) if len(stack) == 0 else str(keyword2index[stack[len(stack)-1]])

                    if key not in mindmap.graph.keys():
                        mindmap.graph[key] = [keyword2index[word]]
                    else:
                        mindmap.graph[key].append(keyword2index[word])
                    stack.append(word)
        return mindmap

    def get_mindmap(self, document: Document, keywords: List[str]) -> MindMap:
        self.llm.set_document(document)
        answer = self.llm.request(self.prompt % keywords).content
        print(answer)
        answer = self.delete_stopwords(answer)
        return self.parse_html(answer, keywords)