import logging
import os
from typing import List

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Product, User

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/generate_ereceipt")
async def generate_ereceipt(products: List[Product], customer: User):
    products_json = [product.reprJSON() for product in products]
    logger.warning("Obtained info about products: %s", products_json)
    logger.warning("Obtained info about customer: %s", customer.reprJSON())
    logger.warning("Generating e-receipt...")
    ereceipt = f"Products: {products_json}, customer: {customer.reprJSON()}".encode(
        "utf-8"
    )
    logger.warning("E-receipt generated")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ereceipt": ereceipt})
