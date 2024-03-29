from fastapi import APIRouter, Depends

from app.schemas.context import Text
from app.schemas.database import DatabaseInfo
from app.controller.summary import SummaryController

from app.api.deps import get_summary_controller, get_s3_controller
import botocore
from langchain.document_loaders import PyPDFLoader, TextLoader

from app.core.config import (
    S3_PREFIX,
    S3_BUCKET_NAME
)

router = APIRouter()

@router.post("/summary", response_model=Text)
def get_summary(
    db: DatabaseInfo, 
    summary_controller: SummaryController = Depends(get_summary_controller),
    s3_controller: botocore.client = Depends(get_s3_controller)
    ) -> Text:

    s3_controller.download_file(S3_BUCKET_NAME, S3_PREFIX + db.key, f'app/static/{db.key}')
    if db.key.split('.')[-1] == "pdf":
        loader = PyPDFLoader(f'app/static/{db.key}')
    else:
        loader = TextLoader(f'app/static/{db.key}')
    
    doc = loader.load_and_split()
    doc = ' '.join(list(map(lambda page: page.page_content,doc)))
    result = summary_controller.transform(doc)
    return Text(summary=result)