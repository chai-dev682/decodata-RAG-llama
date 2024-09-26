from typing import Optional, List
from pydantic import HttpUrl, BaseModel
from datetime import datetime
from enum import Enum


class Message(BaseModel):
    role: str
    content: str

