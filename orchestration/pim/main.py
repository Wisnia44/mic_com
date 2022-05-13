import logging
import os
from typing import List

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Product

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/get_prices")
async def calculate_prices(products: List[Product]):
    logger.warning("Obtained request to get products prices")
    logger.warning("Calculating...")
    products[0].price = 299
    products[1].price = 799
    products_with_prices_json = [product.reprJSON() for product in products]
    logger.warning("Products with calculated prices: %s", products_with_prices_json)
    logger.warning("Requesting receipt service to print receipt")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://receipt_choreography:8008/products_info",
            json=products_with_prices_json,
        )
    logger.warning("Requesting e-receipt service to generate e-receipt")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://ereceipt_choreography:8004/products_info",
            json=products_with_prices_json,
        )
    logger.warning("Requesting payment service to realize payment")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://payments_choreography:8006/products_info",
            json=products_with_prices_json,
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=products_with_prices_json
    )
