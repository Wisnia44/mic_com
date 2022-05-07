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


@app.post("/open")
async def open_doors():
    logger.warning("Doors requested to open")
    logger.warning("Opening doors...")
    logger.warning("Doors opened")
    return JSONResponse(status_code=status.HTTP_200_OK)
