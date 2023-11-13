from fastapi import APIRouter, Depends

from app.schemas.database import DatabaseInfo
from app.schemas.context import Keywords
from app.controller.llm import LLMController
from app.controller.keywords import KeywordsController
from app.api.deps import get_s3_controller
import botocore
from langchain.document_loaders import PyPDFLoader, TextLoader

from app.core.config import (
    S3_PREFIX,
    S3_BUCKET_NAME
)

router = APIRouter()

@router.post("/keywords", response_model=None)
def get_keywords(
    db: DatabaseInfo,
    s3_controller: botocore.client = Depends(get_s3_controller)
    ) -> Keywords:
    
    s3_controller.download_file(S3_BUCKET_NAME, S3_PREFIX + db.key, f'app/static/{db.key}')

    llm_controller = LLMController()
    keyword_controller = KeywordsController(llm_controller)

    if db.key.split('.')[-1] == "pdf":
        loader = PyPDFLoader(f'app/static/{db.key}')
    else:
        loader = TextLoader(f'app/static/{db.key}')
        
    doc = loader.load_and_split()
    return keyword_controller.get_keywords(doc)