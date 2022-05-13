import logging
import os
from typing import List, Union

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
async def verify_card(card: Card):
    logger.warning("Card verification request got")
    logger.warning("Verifying card...")
    logger.warning("Card verification successfull")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.post("/realize_payment")
async def realize_payment():
    logger.warning("Realizing payment...")
    logger.warning("Payment realized")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
