from motor.motor_asyncio import AsyncIOMotorClient
from app.models import User, Role

from bson import ObjectId

client = AsyncIOMotorClient("mongodb+srv://sushanttarapure:c5WIPD6KYtcw5YGJ@sushantati1.derguct.mongodb.net/")
db = client["notes"]

async def get_user(username: str):
    user = await db["users"].find_one({"username": username})
    if user:
        return User(**user)

async def create_user(user: User):
    await db["users"].insert_one(user.dict(by_alias=True))

async def get_role(role_id: str):
    role = await db["roles"].find_one({"_id": ObjectId(role_id)})
    if role:
        return Role(**role)

async def create_role(role: Role):
    await db["roles"].insert_one(role.dict(by_alias=True))
