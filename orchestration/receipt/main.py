import logging
import os
from typing import List, Union

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Product, User

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

info: dict[str, Union[User, List[Product]]] = {"user": None, "products": []}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/print_receipt")
async def print_receipt(products: List[Product], customer: User) -> None:
    products_json = [product.reprJSON() for product in products]
    logger.warning("Obtained info about products: %s", products_json)
    logger.warning("Obtained info about customer: %s", customer.reprJSON())
    logger.warning("Printing receipt...")
    logger.warning("Receipt printed")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
