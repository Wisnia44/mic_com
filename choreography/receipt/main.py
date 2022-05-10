import logging
import os
from typing import List

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
        print_receipt()
    return JSONResponse(status_code=status.HTTP_200_OK, content=products)


@app.post("/customer_info")
async def get_customer_info(customer: User):
    logger.warning("Obtained request with info about the customer")
    customer_info = customer
    if products_info:
        print_receipt()
    return JSONResponse(status_code=status.HTTP_200_OK, content=customer.reprJSON())


async def print_receipt() -> None:
    logger.warning(
        "Obtained info about products, first product=", products_info[0].reprJSON()
    )
    logger.warning("Obtained info about customer: %s", customer_info.reprJSON())
    logger.warning("Printing receipt...")
    logger.warning("Receipt printed")
    customer_info = None
    products_info: List[Product] = []
    return None
