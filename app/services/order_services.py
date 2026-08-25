from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.cart_services import get_cart ,clear_cart
from app.models.order import Order
import logging


logger =logging.getLogger(__name__)

async def place_order(
    mysql_db:Session,
    mongo_db:AsyncIOMotorDatabase,
    user_id:int,
    backgroundtasks:BackgroundTasks):
    cart =await get_cart(mongo_db ,user_id)
    
    if not cart["items"]:
        return None,"cart is Empty"
    
    order_item = []
    for item in cart["items"]:
        order_item.append({
            "product_id":item["product_id"],
            "product_name":item["product_name"],
            "price":item["price"],
            "quantity":item["quantity"],
            "subtotal":item["subtotal"]
        })
    new_order=Order(
        user_id=user_id,
        total=cart["total"],
        status="pending"
    )
    mysql_db.add(new_order)
    mysql_db.commit()
    mysql_db.refresh(new_order)
    
    await mongo_db.orders.insert_one({
        "order_id":new_order.id,
        "user_id":user_id,
        "items":order_item,
        "total":cart["total"],
        "status":"pending",
        "created_at":datetime.utcnow()
    })
    
    await clear_cart(mongo_db,user_id)
    backgroundtasks.add_task(
        send_order_conformation,
        order_id=new_order.id,
        user_id=user_id,
        total=cart["total"]
    )
    order_detail=await mongo_db.orders.find_one({"order_id":new_order.id})
    order_detail["id"]=order_detail["order_id"]
    del order_detail["order_id"]
    del order_detail["_id"]
    
    return order_detail , None

async def get_order_history(
    mysql_db:Session,
    mongo_db:AsyncIOMotorDatabase,
    user_id:int
):
    orders =await mongo_db.orders.find(
        {"user_id":user_id}).sort("created_at",-1).to_list(length=50)
    formatted = []
    for order in orders:
        order["id"]=order["order_id"]
        del order["order_id"]
        del order["_id"]
        formatted.append(order)
        
    return formatted
def send_order_conformation(user_id :int , order_id:int,total:float):
    logger.info(f"Order Conformation - Order #{order_id} plased by user#{user_id}. Total: {total}")
    print(f"Email sent for Order #{order_id} - Total:{total}")
