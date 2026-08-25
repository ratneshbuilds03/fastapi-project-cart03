from fastapi import HTTPException , APIRouter ,status ,Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.mongodb import get_mongodb
from app.schemas.cart import CartItem , CartResponse
from app.services.cart_services import (
    get_cart,add_to_cart,remove_from_cart,clear_cart)
from app.models.user import User
from app.utils.dependencies import get_current_user

router=APIRouter(prefix="/cart",tags=["Cart"])


@router.get("/",response_model=CartResponse)
async def view_cart(
    db:AsyncIOMotorDatabase =Depends(get_mongodb),
    current_user:User=Depends(get_current_user)
):
    return await get_cart(db,current_user.id)

@router.post("/add",response_model=CartResponse)
async def add_item(
    item:CartItem,
    db:AsyncIOMotorDatabase=Depends(get_mongodb),
    current_user:User=Depends(get_current_user)
):
    cart,error= await add_to_cart(db ,current_user.id ,item.product_id,item.quantity)
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return cart

@router.delete("/remove/{product_id}",response_model=CartResponse)
async def remove_item(
    product_id:str,
    db:AsyncIOMotorDatabase=Depends(get_mongodb),
    current_user:User=Depends(get_current_user)
):
    cart ,error = await remove_from_cart(db,current_user.id,product_id)
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    return cart

@router.delete("/clear",status_code=status.HTTP_204_NO_CONTENT)
async def clear_user_cart(
    db:AsyncIOMotorDatabase=Depends(get_mongodb),
    current_user:User=Depends(get_current_user)
):
    await clear_cart(db,current_user.id)


