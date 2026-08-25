from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class OrderItem(BaseModel):
    product_id:str
    product_name:str
    price:float
    quantity:int
    subtotal:float
    
class OrderResponse(BaseModel):
    id :int
    user_id:int
    items:List[OrderItem]
    total:float
    status:str
    created_at:Optional[datetime]
    