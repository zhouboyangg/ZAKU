from fastapi import FastAPI, HTTPException
from .init import app  # Import the FastAPI app instance
from .models import Conversation, QueryResponse  # Import the Beanie models
from typing import List

@app.post("/conversations", response_model=Conversation)
async def create_conversation(conversation: Conversation):
    await conversation.save()
    return conversation

@app.get("/conversations", response_model=List[Conversation])
async def get_conversations():
    return await Conversation.find_all().to_list()

@app.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    conversation = await Conversation.get(conversation_id)
    if conversation:
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@app.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(conversation_id: str, updated_conversation: Conversation):
    conversation = await Conversation.get(conversation_id)
    if conversation:
        conversation.update(updated_conversation)
        await conversation.save()
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    conversation = await Conversation.get(conversation_id)
    if conversation:
        await conversation.delete()
        return {"message": "Conversation deleted successfully"}
    raise HTTPException(status_code=404, detail="Conversation not found")

  

