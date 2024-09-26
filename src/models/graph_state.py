from typing import Optional, List
from pydantic import BaseModel
from models import Message

class GraphState(BaseModel):
    messages: List[Message]
    query: Optional[str] = None
