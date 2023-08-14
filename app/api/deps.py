from typing import Optional
from app.controller.mindmap import MindMapController
import torch
import esupar

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mindmap_controller: Optional[MindMapController] = None

def init_model() -> None:
    global mindmap_controller
    
    nlp_model = nlp=esupar.load("KoichiYasuoka/roberta-large-korean-morph-upos")
    mindmap_controller = MindMapController(nlp_model)

def get_mindmap_model() -> MindMapController:
    return mindmap_controller