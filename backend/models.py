from beanie import Document
from pydantic import Field, BaseModel
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
    id: Optional[str] = Field(default=None, alias="_id", description="ID of the conversation")  # MongoDB automatically provides this
    name: str = Field(..., max_length=200, description="Title of the conversation")
    params: Dict = Field(default={}, description="Parameter dictionary for overriding defaults prescribed by the AI Model")
    tokens: Optional[int] = Field(default=0, ge=0, description="Total number of tokens consumed in this entire Chat")
    pinned: bool = Field(default=False, description="Indicates if the conversation is pinned")
    prompts: List[Prompt] = Field(default=[], description="List of prompts associated with the conversation")
    model: str = Field(..., description="Model identifier for the conversation")
    modifications: List[str] = Field(default=[], description="List of modifications applied to the conversation")
    class Settings:
      collection_name = "conversations"

class ConversationPOST(BaseModel):  # Changed to inherit from BaseModel
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

class ConversationPUT(BaseModel):  # Changed to inherit from BaseModel
    name: Optional[str] = Field(None, max_length=200)
    params: Optional[Dict] = Field(None)