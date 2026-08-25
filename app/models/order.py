from sqlalchemy import Float,String,Integer ,Column ,DateTime ,ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__="orders"
    
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    total=Column(Float,nullable=False)
    status =Column(String(50),default="pending")
    created_at= Column(DateTime(timezone=True),server_default=(func.now()))