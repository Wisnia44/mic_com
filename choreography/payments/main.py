import logging
import os
from typing import List, Union

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Card, Product, User

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

info: dict[str, Union[User, List[Product]]] = {"user": None, "products": []}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/verify_card")
async def verify_card(card: Card, user: User):
    logger.warning("Card verification request got")
    logger.warning("Verifying card...")
    logger.warning("Card verification successfull")
    logger.warning("Sending request to CRM with successfully verified card")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://crm_choreography:8002/card_verified",
            json=user.reprJSON(),
        )
    return JSONResponse(status_code=status.HTTP_200_OK)


@app.post("/products_info")
async def get_products_info(products: list[Product]):
    logger.warning("Obtained request with info about products containing prices")
    info["products"] = products
    if info["user"]:
        await realize_payment()
    else:
        logger.warning("Waiting for customer info to realize payment")
    return JSONResponse(status_code=status.HTTP_200_OK)


@app.post("/customer_info")
async def get_customer_info(customer: User):
    logger.warning("Obtained request with info about the customer")
    info["user"] = customer
    if info["products"]:
        await realize_payment()
    else:
        logger.warning("Waiting for products info to realize payment")
    return JSONResponse(status_code=status.HTTP_200_OK, content=customer.reprJSON())


async def realize_payment() -> None:
    logger.warning(
        "Obtained info about products, first product=%s", info["products"][0].reprJSON()
    )
    logger.warning("Obtained info about customer: %s", info["user"].reprJSON())  # type: ignore [union-attr]
    logger.warning("Realizing payment...")
    logger.warning("Payment realized")
    info["user"] = None
    info["products"] = []
    return None
