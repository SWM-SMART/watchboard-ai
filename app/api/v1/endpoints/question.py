from fastapi import APIRouter, Depends

from app.schemas.context import Text, Context
from app.controller.llm import LLMController

from app.api.deps import get_llm_controller
router = APIRouter()

@router.post("/question", response_model=Text)
def get_answer(context: Context, controller: LLMController = Depends(get_llm_controller)) -> Text:
    question = f"'{context.summary}'에서 {context.keyword}의 의미를 알려줘"
    return Text(text=controller.request_base(question))