from typing import Optional

from app.controller.llm import LLMController
from app.controller.mindmap import MindMapController
from app.controller.keywords import KeywordsController
from app.controller.summary import SummaryController

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from app.core.config import (
    SUMMARY_MODEL_PATH,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
import torch
import nltk
import boto3

from fastapi import Depends

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mindmap_controller: Optional[MindMapController] = None
summary_model: Optional[AutoTokenizer] = None

def init_model() -> None:
    global summary_model, summary_tokenizer, summary_controller, llm_controller, mindmap_controller, keyword_controller, s3_controller
    
    nltk.download('punkt')
    summary_model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARY_MODEL_PATH)
    summary_tokenizer = AutoTokenizer.from_pretrained(SUMMARY_MODEL_PATH)
    summary_controller = SummaryController(summary_model, summary_tokenizer)

    llm_controller = LLMController()
    mindmap_controller = MindMapController(llm_controller)
    keyword_controller = KeywordsController(llm_controller)
    
    s3_controller = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2", # 자신이 설정한 bucket region
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    

def get_summary_model() -> AutoModelForSeq2SeqLM:
    return summary_model

def get_summary_tokenizer() -> AutoTokenizer:
    return summary_tokenizer

def get_summary_controller(
        model: AutoModelForSeq2SeqLM = Depends(get_summary_model), 
        tokenizer: AutoTokenizer = Depends(get_summary_tokenizer)
    ) -> SummaryController:
    global summary_controller
    if summary_controller is None:
        summary_controller = SummaryController(model, tokenizer)
    return summary_controller

def get_llm_controller() -> LLMController():
    return llm_controller

def get_mindmap_controller() -> MindMapController():
    return mindmap_controller

def get_keyword_controller() -> KeywordsController():
    return keyword_controller

def get_s3_controller():
    return s3_controller