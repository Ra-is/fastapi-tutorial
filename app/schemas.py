from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint


class UserResponse(BaseModel):
    id: int
    email:str
    created_at: datetime
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
   pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    onwer: UserResponse
    class Config:
        from_attributes = True
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)