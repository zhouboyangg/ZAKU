from fastapi import HTTPException, APIRouter
from models import Conversation, Prompt, ConversationPOST, ConversationPUT
from typing import List
from services import send_prompt_to_chatgpt
import httpx

router = APIRouter()

@router.get("/")
async def root():
    return {"Hello": "World"}

@router.post("/conversations", response_model=ConversationPOST)
async def create_conversation(conversation_data: Conversation):
    conversation = Conversation(**conversation_data.dict())
    await conversation.save()
    return conversation

@router.get("/conversations", response_model=List[Conversation])
async def get_conversations():
    conversations = await Conversation.find().to_list()
    return conversations

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    # Retrieve a single Conversation document by ID
    conversation = await Conversation.find_one(Conversation.id == conversation_id)
    if conversation:
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@router.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(conversation_id: str, conversation_update: ConversationPUT):
    # Find and update a Conversation document by ID
    conversation = await Conversation.find_one(Conversation.id == conversation_id)
    if conversation:
        # Update and save the document with new data
        for key, value in conversation_update.dict(exclude_unset=True).items():
            setattr(conversation, key, value)
        await conversation.save()
        return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    # Delete a Conversation document by ID
    conversation = await Conversation.find_one(Conversation.id == conversation_id)
    if conversation:
        await conversation.delete()
        return {"message": "Conversation deleted successfully"}
    raise HTTPException(status_code=404, detail="Conversation not found")

@router.post("/queries")
async def create_prompt_query(prompt: Prompt):
    try:
        # Extract the prompt content and send it to ChatGPT via the OpenAI API
        prompt_text = prompt.content
        response_data = await send_prompt_to_chatgpt(prompt_text)
        # Here, you could also insert the query and response into a MongoDB collection if desired
        # For example, save the query and response in a `queries` collection for logging or analysis
        return {"response": response_data}
    except httpx.HTTPStatusError as http_exc:
        detail = f"HTTP error occurred: {http_exc.response.status_code}"
        raise HTTPException(status_code=422, detail=detail)
    except Exception as e:
        print(f"Error sending prompt to ChatGPT: {str(e)}")
        raise HTTPException(status_code=422, detail="Error processing the ChatGPT query")
    