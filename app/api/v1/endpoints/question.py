from fastapi import APIRouter, Depends

from app.schemas.context import Text, Context
from app.controller.llm import LLMController

router = APIRouter()

@router.post("/question", response_model=Text)
def get_answer(context: Context) -> Text:
    controller = LLMController()
    question = f"'{context.summary}'에서 {context.keyword}의 의미를 알려줘"
    return Text(text=controller.request_base(question))