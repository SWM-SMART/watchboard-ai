from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.controller.llm import LLMController
from app.controller.mindmap import MindMapController
from app.schemas.mindmap import MindMap
from app.schemas.document import Document

from app.api.deps import get_s3_controller
import botocore
from langchain.document_loaders import PyPDFLoader, TextLoader

from app.core.config import (
    S3_PREFIX,
    S3_BUCKET_NAME
)

router = APIRouter()

@router.post("/mindmap", response_model=None)
def get_mind_map(
    document: Document, 
    s3_controller: botocore.client = Depends(get_s3_controller)
    ) -> MindMap:

    s3_controller.download_file(S3_BUCKET_NAME, S3_PREFIX + document.key, f'app/static/{document.key}')

    llm_controller = LLMController()
    mindmap_controller = MindMapController(llm_controller)

    if document.key.split('.')[-1] == "pdf":
        loader = PyPDFLoader(f'app/static/{document.key}')
    else:
        loader = TextLoader(f'app/static/{document.key}')
    doc = loader.load_and_split()
    if len(doc) == 0: return HTTPException(status_code=404, detail="Error")
    ret = mindmap_controller.get_mindmap(doc, document.keywords)
    print(ret)
    return ret
