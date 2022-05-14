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


@app.post("/products_info")
async def get_products_info(products: list[Product]):
    logger.warning("Obtained request with info about products containing prices")
    info["products"] = products
    if info["user"]:
        await print_receipt()
    else:
        logger.warning("Waiting for products info to print receipt")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.post("/customer_info")
async def get_customer_info(customer: User):
    logger.warning("Obtained request with info about the customer")
    info["user"] = customer
    if info["products"]:
        await print_receipt()
    else:
        logger.warning("Waiting for products info to print receipt")
    return JSONResponse(status_code=status.HTTP_200_OK, content=customer.reprJSON())


async def print_receipt() -> None:
    logger.warning(
        "Obtained info about products, first product=%s", info["products"][0].reprJSON()
    )
    logger.warning("Obtained info about customer: %s", info["user"].reprJSON())  # type: ignore [union-attr]
    logger.warning("Printing receipt...")
    logger.warning("Receipt printed")
    info["user"] = None
    info["products"] = []
    return None
