import logging
import os

from checkout import router as checkout_router
from entering import router as entering_router
from fastapi import FastAPI, status

app = FastAPI()
app.include_router(checkout_router)
app.include_router(entering_router)

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}
