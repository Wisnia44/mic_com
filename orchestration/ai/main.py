import logging
import os

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import ProductId
from shared.utils import product1, product2

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.get("/get_purchased_products")
async def get_purchased_products():
    logger.warning("Obtained request to get purchased products info on checkout")
    logger.warning("Analysing...")
    products_ids = [
        ProductId(id=product1.id).reprJSON(),
        ProductId(id=product2.id).reprJSON(),
    ]
    logger.warning("Calculated products ids: %s", products_ids)
    return JSONResponse(status_code=status.HTTP_200_OK, content=products_ids)
