import logging
import os

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Card, User

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/scan_again")
async def scan_again(user: User):
    logger.warning("Second scan request got")
    logger.warning("Enabling second scan")
    logger.warning("Waiting for the user to scan the card...")
    logger.warning("Second scan detected")
    card = Card(card_token="123abc123")
    return JSONResponse(status_code=status.HTTP_200_OK, json=card.reprJSON())
