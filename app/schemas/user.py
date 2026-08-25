from pydantic import BaseModel, EmailStr,Field
from typing import Optional

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str = Field(...,min_length=1,max_length=72) 
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    
class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    class config:
        from_attributes =True
    
class Token(BaseModel):
    access_token:str
    token_type:str="bearer"
    
class TokenData(BaseModel):
    user_id: Optional[int]= None