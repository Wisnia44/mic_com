import logging
import os

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from payments.queue_processor import PAYMENT_QUEUE, process_realize_payment_queue
from shared.models import Card, Product, User

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))
process_realize_payment_queue(10)


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
        client.post(
            "http://crm_choreography:8002/card_verified",
            json=user.reprJSON(),
        )
    return JSONResponse(status_code=status.HTTP_200_OK)


@app.post("/products_info")
async def get_products_info(products_json: list[Product]):
    logger.warning("Obtained request with info about products containing prices")
    products = [
        Product(
            name=product["name"],
            price=product["price"],
            quantity=product["quantity"],
        )
        for product in products_json
    ]
    PAYMENT_QUEUE["products"] = products
    return JSONResponse(status_code=status.HTTP_200_OK, content=products_json)


@app.post("/customer_info")
async def get_customer_info(customer: User):
    logger.warning("Obtained request with info about the customer")
    PAYMENT_QUEUE["customer"] = customer
    return JSONResponse(status_code=status.HTTP_200_OK, content=customer.reprJSON())
