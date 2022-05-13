import logging
import os

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.get("/open")
async def open_doors():
    logger.warning("Doors requested to open")
    logger.warning("Opening doors...")
    logger.warning("Doors opened")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.get("/customer_exit")
async def customer_exited():
    logger.warning("Customer went out of the store")
    logger.warning("Notifying orchestrator")
    async with httpx.AsyncClient() as client:
        await client.get("http://orchestrator_orchestration:8000/checkout")
    return JSONResponse(status_code=status.HTTP_200_OK)
