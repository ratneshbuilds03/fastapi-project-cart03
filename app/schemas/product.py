from datetime import datetime
from typing import Optional
from pydantic import BaseModel , Field

class ProductCreate(BaseModel):
    name:str=Field(..., min_length=1,max_length=200)
    description:Optional[str]=None
    price:float=Field(...,gt=0)
    category:str
    stock: int=Field(...,ge=0)
    image:Optional[str]=None
class ProductUpdate(BaseModel):
    name:Optional[str]=Field(None,min_length=1,max_length=200)
    description:Optional[str]=None
    price:Optional[float]=Field(None,gt=0)
    category:Optional[str]=None
    stock:Optional[int]=Field(None,ge=0)
    image:Optional[str]=None
    
class ProductResponse(BaseModel):
    id:str
    name:str
    description:Optional[str] =None
    price:float
    category:str
    stock:int
    image:Optional[str]=None
    created_at:Optional[datetime] = None