import logging
from fastapi import Request,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

async def validation_exception_handler(request:Request,exc:RequestValidationError):
    errors =[]
    for error in exc.errors():
        errors.append({
            "field":error["loc"][-1],
            "meassage":error["msg"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail":"validation failed","errors":errors}
    )
    
async def sqlalchemy_exception_handler(request:Request,exc:SQLAlchemyError):
    logger.error(f"Database error :{str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail":"Database error occurred"}
    )
    
async def general_exception_handler(request:Request,exc:Exception):
    logger.error(f"Unexpected error :{str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail":"An unexpected error occurred"}
    )