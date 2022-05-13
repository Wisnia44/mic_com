import logging
import os

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.utils import get_products_json

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
    products_json = get_products_json()
    logger.warning("Calculated products info: %s", products_json)
    return JSONResponse(status_code=status.HTTP_200_OK, content=products_json)
