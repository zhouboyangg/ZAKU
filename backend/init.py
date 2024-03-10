from contextlib import asynccontextmanager
from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .models import Conversation, QueryResponse
app = FastAPI()

DATABASE_URL = "mongodb+srv://zhouboyangg:HN4iSnp4aDMZUxCm@zaku.xdaco00.mongodb.net/?authMechanism=DEFAULT"

client = AsyncIOMotorClient(DATABASE_URL)
db = client.ZAKU  # Replace with your database name

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(database=db, document_models=[Conversation, QueryResponse])