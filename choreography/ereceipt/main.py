import logging
import os
from typing import List

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Product, User

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

customer_info: User = None
products_info: List[Product] = []


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/products_info")
async def get_products_info(products: list[Product]):
    logger.warning("Obtained request with info about products containing prices")
    products_info = products
    if customer_info:
        await generate_ereceipt()
    return JSONResponse(status_code=status.HTTP_200_OK, content=products)


@app.post("/customer_info")
async def get_customer_info(customer: User):
    logger.warning("Obtained request with info about the customer")
    customer_info = customer
    if products_info:
        await generate_ereceipt()
    return JSONResponse(status_code=status.HTTP_200_OK, content=customer.reprJSON())


async def generate_ereceipt() -> None:
    logger.warning(
        "Obtained info about products, first product=", products_info[0].reprJSON()
    )
    logger.warning("Obtained info about customer: %s", customer_info.reprJSON())
    logger.warning("Generating e-receipt...")
    logger.warning("E-receipt generated")
    logger.warning("Requesting message service to send e-receipt to the customer")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://messages_choreography:8005/send_ereceipt",
            json=customer_info.reprJSON(),
        )
    customer_info = None
    products_info: List[Product] = []
    return None
