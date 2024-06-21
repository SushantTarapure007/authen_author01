from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    roles: List[str]

class RoleCreate(BaseModel):
    name: str
    permissions: List[str]

class RoleResponse(BaseModel):
    id: str
    name: str
    permissions: List[str]

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')
