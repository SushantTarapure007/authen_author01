from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId

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
    def __get_pydantic_json_schema__(cls, schema, handler):
        schema.update(type='string')
        return schema

class User(BaseModel):
    id: PyObjectId | str = Field(default_factory=PyObjectId, alias="_id")
    username: str
    hashed_password: str
    roles: List[str] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Role(BaseModel):
    id: PyObjectId | str = Field(default_factory=PyObjectId, alias="_id")
    name: str
    permissions: List[str] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
