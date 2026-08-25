from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

db = None
client = None 

async def connect_mongodb():
    global client , db 
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB]
    print("Mongodb Connect Succsessfully")
    
async def close_mongodb():
    global client
    if client:
        client.close()
        print("MongoDB Connection Close")
        
def get_mongodb():
    return db