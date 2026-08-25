from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.product import ProductCreate , ProductResponse , ProductUpdate

async def create_product(db:AsyncIOMotorDatabase , product_data:ProductCreate):
    product_dict=product_data.model_dump()
    product_dict["created_at"]=datetime.utcnow()
    
    result =await db.products.insert_one(product_dict)
    
    created = await db.products.find_one({"_id":result.inserted_id})
    return format_product(created)

async def get_all_products(db:AsyncIOMotorDatabase):
    products = await db.products.find().to_list(length=100)
    return [format_product(p) for p in products]

async def get_product_by_id(db:AsyncIOMotorDatabase,product_id:str):
    try:
        product = await db.products.find_one({"_id":ObjectId(product_id)})
        return format_product(product) if product else None
    except Exception:
        return None

async def update_product(db:AsyncIOMotorDatabase,product_id:str,product_data:ProductUpdate):
    update_data = {k: v for k ,v in product_data.model_dump(exclude_unset=True).items() }#if v is not None}
    if not update_data:
        return await get_product_by_id(db,product_id)
    
    await db.products.update_one(
        {"_id":ObjectId(product_id)},
        {"$set":update_data}
    )
    
    return await get_product_by_id(db,product_id)

async def delete_product(db:AsyncIOMotorDatabase,product_id:str):
    result = await db.products.delete_one({"_id":ObjectId(product_id)})
    return result.deleted_count > 0

def format_product(product:dict) -> dict :
    if product:
        product ["id"]= str(product["_id"])
        del product["_id"]
        if "creaated_at" in product:
            product["created_at"] = product.pop("creaated_at")
    return product
