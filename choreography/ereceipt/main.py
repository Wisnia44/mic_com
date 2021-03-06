import logging
import os
from typing import List, Union

import httpx
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
    if info["customer"]:
        await generate_ereceipt()
    else:
        logger.warning("Waiting for customer info to generate e-receipt")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.post("/customer_info")
async def get_customer_info(customer: User):
    logger.warning("Obtained request with info about the customer")
    info["customer"] = customer
    if info["products"]:
        await generate_ereceipt()
    else:
        logger.warning("Waiting for products info to generate e-receipt")
    return JSONResponse(status_code=status.HTTP_200_OK, content=customer.reprJSON())


async def generate_ereceipt() -> None:
    logger.warning(
        "Obtained info about products, first product=%s", info["products"][0].reprJSON()
    )
    logger.warning("Obtained info about customer: %s", info["customer"].reprJSON())  # type: ignore [union-attr]
    logger.warning("Generating e-receipt...")
    logger.warning("E-receipt generated")
    logger.warning("Requesting message service to send e-receipt to the customer")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://messages_choreography:8005/send_ereceipt",
            json=info["customer"].reprJSON(),  # type: ignore [union-attr]
        )
    info["customer"] = None
    info["products"] = []
    return None
