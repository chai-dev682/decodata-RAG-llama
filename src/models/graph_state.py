from typing import Optional, List
from pydantic import BaseModel
from src.models.models import Message

class GraphState(BaseModel):
    messages: List[Message]
    query: Optional[str] = None
