from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import Conversation, ConversationPOST, ConversationPUT, QueryRoleType
from routes import router as api_router

app = FastAPI(title="Test Project", version="1.0")
# Database Configuration
DATABASE_URL = "mongodb+srv://zhouboyangg:HN4iSnp4aDMZUxCm@zaku.xdaco00.mongodb.net/?authMechanism=DEFAULT"
client = AsyncIOMotorClient(DATABASE_URL)
db = client["ZAKU"] 

@app.on_event("startup")
async def startup_event():
    await init_beanie(database=db, document_models=[Conversation])
    print("Beanie initialized.")

# Setup CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include API Router
app.include_router(api_router)

