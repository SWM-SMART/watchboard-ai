from typing import Optional

from fastapi import APIRouter, Depends

from app.controller.mindmap import MindMapController
from app.schemas.mindmap import MindMap
from app.schemas.document import Document

from app.api.deps import get_mindmap_controller, get_s3_controller
import botocore
from langchain.document_loaders import PyPDFLoader

from app.core.config import (
    S3_PREFIX,
    S3_BUCKET_NAME
)

router = APIRouter()

@router.post("/mindmap", response_model=None)
def get_mind_map(
    document: Document, 
    mindmap_controller: MindMapController = Depends(get_mindmap_controller),
    s3_controller: botocore.client = Depends(get_s3_controller)
    ) -> MindMap:

    s3_controller.download_file(S3_BUCKET_NAME, S3_PREFIX + document.dbInfo.key, f'app/static/{document.dbInfo.key}')
    loader = PyPDFLoader(f'app/static/{document.dbInfo.key}')
    doc = loader.load_and_split()
    return mindmap_controller.get_mindmap(doc, document.keywords)
