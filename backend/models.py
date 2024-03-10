from beanie import Document
from pydantic import Field
from typing import List, Dict, Optional
from enum import Enum

class QueryRoleType(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"

class Prompt(Document):
    role: QueryRoleType
    content: str

class Conversation(Document):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., max_length=200)
    params: Dict = Field(default={})
    tokens: Optional[int] = Field(default=0, ge=0)
    messages: List[Prompt] = Field(default=[])

    class Settings:
        name = "Conversation"

class ConversationPOST(Document):
    name: str = Field(..., max_length=200)
    params: Dict = Field(default={})
    model: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "My Conversation",
                "params": {},
                "model": "default_model"
            }
        }

class ConversationPUT(Document):
    name: Optional[str] = Field(None, max_length=200)
    params: Optional[Dict] = Field(None)