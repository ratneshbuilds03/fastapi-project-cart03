from typing import List ,Optional
from pydantic import BaseModel , Field

class CartItem(BaseModel):
    product_id : str
    quantity:int = Field(...,gt=0)
    
class CartItemResponse(BaseModel):
    product_id:str
    product_name:str
    price:float
    quantity:int
    subtotal:float
    
class CartResponse(BaseModel):
    user_id:int 
    items:List[CartItemResponse]=[]
    total:float=0.0
    total_item:int=0