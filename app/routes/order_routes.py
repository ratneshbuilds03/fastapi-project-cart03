from fastapi import APIRouter,HTTPException ,status ,Depends ,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.mongodb import get_mongodb
from app.schemas.order import OrderResponse
from app.services.order_services import place_order ,get_order_history
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders",tags=["Orders"])

@router.post("/place",response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
async def created_order(
    background_tasks:BackgroundTasks,
    mysql_db:Session=Depends(get_db),
    mongo_db:AsyncIOMotorDatabase =Depends(get_mongodb),
    current_user:User=Depends(get_current_user)
):
    order ,error =await place_order(
        mysql_db,
        mongo_db,
        current_user.id,
        background_tasks,
    )
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return order

@router.get("/history",response_model=List[OrderResponse])
async def order_history(
    mysql_db:Session=Depends(get_db),
    mongo_db:AsyncIOMotorDatabase=Depends(get_mongodb),
    current_user:User=Depends(get_current_user)
):
    return await get_order_history(mysql_db,mongo_db,current_user.id)