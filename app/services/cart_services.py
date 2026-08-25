from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.product_service import get_product_by_id

async def get_cart(db:AsyncIOMotorDatabase,user_id:int):
    cart = await db.carts.find_one({"user_id":user_id})
    if not cart:
        return({"user_id":user_id,"items":[],"total":0.0,"total_item":0})
    return await format_cart(db,cart)

async def add_to_cart(db:AsyncIOMotorDatabase,user_id:int,product_id:str,quantity:int):
    product=await get_product_by_id(db,product_id)
    if not product:
        return None ,"Product not found"
    if product["stock"]< quantity:
        return None ,f"Only {product['stock']}items available in Stock"
        
    cart = await db.carts.find_one({"user_id":user_id})
    
    if not cart: 
        await db.carts.insert_one({"user_id":user_id,"items":[{"product_id":product_id,"quantity":quantity}]})
    else:
        existing_item=None  
        for item in cart["items"]:
            if item["product_id"]==product_id:
                existing_item = item
                break
        if existing_item:
            new_quantity=existing_item["quantity"]+quantity
            if product["stock"]<new_quantity:
                return None,f"Only{product['stock']} items available"
            await db.carts.update_one(
            {"user_id":user_id,"items.product_id":product_id},
            {"$set":{"items.$.quantity":new_quantity}}
        )
        else:
            await db.carts.update_one(
                {"user_id":user_id},
                {"$push":{"items":{"product_id":product_id,"quantity":quantity}}}
                )
    cart =await db.carts.find_one({"user_id":user_id})
    return await format_cart(db,cart),None
async def remove_from_cart(db:AsyncIOMotorDatabase,user_id:int,product_id :str):
    cart=await db.carts.find_one({"user_id":user_id})
    if not cart:
        return None ,"Cart not found"
    await db.carts.update_one(
        {"user_id":user_id},
        {"$pull":{"items":{"product_id":product_id}}}
    )
    cart =await db.carts.find_one({"user_id":user_id})
    return await format_cart(db,cart),None

async def clear_cart(db:AsyncIOMotorDatabase,user_id:int):
    await db.carts.update_one(
        {"user_id":user_id},
        {"$set":{"items":[]}}
    )
    return True

async def format_cart(db:AsyncIOMotorDatabase,cart:dict):
    formatted_item=[]
    total=0.0
    
    for item in cart.get("items",[]):
        product = await get_product_by_id(db,item["product_id"])
        if product:
            subtotal= product["price"]*item["quantity"]
            total += subtotal
            formatted_item.append({
                "product_id":item["product_id"],
                "product_name":product["name"],
                "price":product["price"],
                "quantity":item["quantity"],
                "subtotal": subtotal
            })
        
    return { 
            "user_id":cart["user_id"],
            "items":formatted_item,
            "total":round(total,2),
            "total_item": len(formatted_item),
            }