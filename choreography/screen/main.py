import logging
import os

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/open_doors")
async def info_open_doors():
    logger.warning("Info about opening doors show request obtained")
    logger.warning("Showing info about opening doors...")
    logger.warning("Info shown")
    return JSONResponse(status_code=status.HTTP_200_OK)
