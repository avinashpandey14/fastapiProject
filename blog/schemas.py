from pydantic import BaseModel
from typing import Optional,List

class Blog(BaseModel):
    title:str
    body:str
    # published:Optional[bool]
    class Config:
        orm_mode = True
    
class User(BaseModel):
    name:str
    email:str
    password:str
    
    class Config:
        orm_mode = True
        
class ShowUser(BaseModel):
    name:str
    email:str
    user:List[Blog]=[]
    class Config:
        orm_mode = True
        
        
class ShowBlog(BaseModel):
    title:str
    body:str
    creator: ShowUser
    
    class Config:
        orm_mode = True
        

class Login(BaseModel):
    username:str
    password:str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None