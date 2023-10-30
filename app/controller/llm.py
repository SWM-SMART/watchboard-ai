from langchain.schema.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough

from langchain import hub

class LLMController:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.rag_prompt = hub.pull("rlm/rag-prompt")
        self.llm = ChatOpenAI(model_name="gpt-4-0613", temperature=0)

    def set_document(self, document: Document) -> None:
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(document)

        docsearch = Chroma.from_documents(texts, self.embeddings)
        retriever = docsearch.as_retriever()

        self.rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | self.rag_prompt
            | self.llm 
        )
    
    def request_base(self, query: str):
        return self.llm.predict(query)

    def request(self, query: str) -> str:
        return self.rag_chain.invoke(query)
