from typing import Optional
from app.controller.mindmap import MindMapController
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mindmap_controller: Optional[MindMapController] = None

def init_model() -> None:
    pass

def get_mindmap_model() -> MindMapController:
    return mindmap_controller