from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.database import Base,engine
from app.mongodb import connect_mongodb ,close_mongodb
from app.middleware.logging_middleware import log_requests
from app.utils.error_handlers import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler)
from app.utils.rate_limiter import limiter
from app.routes.product_route import router as porduct_router
from app.routes.cart_routes import router as cart_router
from app.routes.auth_routes import router as auth_router
from app.routes.order_routes import router as order_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await connect_mongodb()
    Base.metadata.create_all(bind=engine)
    yield   
    await close_mongodb()
    
app = FastAPI(
    title="Cart System API",
    description="E-commerce cart system with FastAPI,MySql and MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

app.middleware("http")(log_requests)

app.add_exception_handler(RequestValidationError,validation_exception_handler)
app.add_exception_handler(SQLAlchemyError,sqlalchemy_exception_handler)
app.add_exception_handler(Exception,general_exception_handler)


app.include_router(porduct_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.get("/")
async def root():
    return {"status":"ok","service":"cart_api"}

@app.get("/health")
async def healt_check():
    return {"status":"ok","service":"cart_api"}

app = CORSMiddleware(
    app=app,
    allow_origins=["https://cartify-pi-nine.vercel.app","http://localhost:3000","http://localhost:8000","http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["Authorization","Content-Type"],
)