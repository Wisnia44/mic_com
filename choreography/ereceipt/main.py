import logging
import os
from typing import Dict, List, Union

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from queue_processor import process_generating_ereceipt_queue
from shared.models import Product, User

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

ERECEIPT_GENERATING_QUEUE: Dict[str, Union[List[Product], User]] = {}
process_generating_ereceipt_queue(10, ERECEIPT_GENERATING_QUEUE)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


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
    ERECEIPT_GENERATING_QUEUE["products"] = products
    return JSONResponse(status_code=status.HTTP_200_OK, content=products_json)


@app.post("/customer_info")
async def get_customer_info(customer: User):
    logger.warning("Obtained request with info about the customer")
    ERECEIPT_GENERATING_QUEUE["customer"] = customer
    return JSONResponse(status_code=status.HTTP_200_OK, content=customer.reprJSON())
