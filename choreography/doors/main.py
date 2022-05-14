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
    logger.warning("Calling CRM to get info about customer")
    async with httpx.AsyncClient() as client:
        await client.get("http://crm_choreography:8002/customer_info")
    logger.warning("Calling AI to get info about purchased products")
    async with httpx.AsyncClient() as client:
        await client.get("http://ai_choreography:8001/get_purchased_products")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
