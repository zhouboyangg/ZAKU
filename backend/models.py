from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class Message(BaseModel):
    sender: str
    message: str
    timestamp: datetime

class Conversation(Document):
    conversationId: str = Field(default_factory=str)
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
    status: str
    messages: List[Message] = []

class QueryResponse(Document):
    queryId: str = Field(default_factory=str)
    queryText: str
    response: str
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
