from fastapi import APIRouter , HTTPException ,status ,Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.mongodb import get_mongodb
from app.schemas.product import ProductUpdate, ProductCreate, ProductResponse
from app.services.product_service import (create_product,
                get_all_products, get_product_by_id,
                update_product, delete_product)

router = APIRouter(prefix="/products",tags=["Products"])

@router.post("/", response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
async def add_product(product:ProductCreate,db:AsyncIOMotorDatabase=Depends(get_mongodb)):
    return await create_product(db,product)

@router.get("/",response_model=List[ProductResponse])
async def list_products(db:AsyncIOMotorDatabase=Depends(get_mongodb)):
    return await get_all_products(db)

@router.get("/{product_id}",response_model=ProductResponse)
async def get_products(product_id:str,db:AsyncIOMotorDatabase=Depends(get_mongodb)):
    product = await get_product_by_id(db,product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found"
        )
    return product

@router.put("/{product_id}",response_model=ProductResponse)
async def edit_products(product_id:str ,product:ProductUpdate,db :AsyncIOMotorDatabase=Depends(get_mongodb)):
    update = await update_product(db,product_id,product)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found"
        )
    return update

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
async def remove_products(product_id:str , db:AsyncIOMotorDatabase=Depends(get_mongodb)):
    success= await delete_product(db,product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Nor Found"
        )