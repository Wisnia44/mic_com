import json
import logging
import os
from typing import List

import httpx
import redis
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Product, ProductId
from shared.utils import populate_products_data

app = FastAPI()
redis_pim = redis.Redis(host="redis_pim_choreography", port=6379)
populate_products_data(redis_pim)

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/get_products")
async def get_products(products_ids: List[ProductId]):
    logger.warning("Obtained request to get products info")
    logger.warning("Getting products from database...")
    products = []
    for id in products_ids:
        product_db = redis_pim.get(id)
        product_dict = json.loads(product_db)  # type: ignore [arg-type]
        product = Product(
            id=product_dict["id"],
            name=product_dict["name"],
            price=product_dict["price"],
        )
        products.append(product.reprJSON())
    logger.warning("All products found in the database")
    logger.warning("Products info: %s", products)

    logger.warning("Requesting receipt service to print receipt")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://receipt_choreography:8008/products_info", json=products
        )

    logger.warning("Requesting e-receipt service to generate e-receipt")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://ereceipt_choreography:8004/products_info", json=products
        )

    logger.warning("Requesting payment service to realize payment")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://payments_choreography:8006/products_info", json=products
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=products)
