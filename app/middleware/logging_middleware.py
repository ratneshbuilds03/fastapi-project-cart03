import logging
from fastapi import Request
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

async def log_requests(request:Request,call_next):
    start_time = time.time()
    
    response= await call_next(request)
    
    process_time = time.time() - start_time
    
    logger.info(
        f"Method:{request.method} | "
        f"URL:{request.url.path} | "
        f"Status:{response.status_code} | "
        f"Time:{process_time:.3f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response