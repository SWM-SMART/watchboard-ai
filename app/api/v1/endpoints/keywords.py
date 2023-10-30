from fastapi import APIRouter, Depends

from app.schemas.document import Document
from app.schemas.context import Keywords
from app.controller.keywords import KeywordsController
from app.api.deps import get_keyword_controller, get_s3_controller
import botocore
from langchain.document_loaders import PyPDFLoader

from app.core.config import (
    S3_PREFIX,
    S3_BUCKET_NAME
)

router = APIRouter()

@router.post("/keywords", response_model=None)
def get_keywords(
    document: Document, 
    keyword_controller: KeywordsController = Depends(get_keyword_controller),
    s3_controller: botocore.client = Depends(get_s3_controller)
    ) -> Keywords:
    
    s3_controller.download_file(S3_BUCKET_NAME, S3_PREFIX + document.dbInfo.key, f'app/static/{document.dbInfo.key}')
    loader = PyPDFLoader(f'app/static/{document.dbInfo.key}')
    doc = loader.load_and_split()
    return keyword_controller.get_keywords(doc)