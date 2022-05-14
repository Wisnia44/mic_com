import logging
import os

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Card, User

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/card_scanned")
async def card_scanned(card: Card):
    logger.warning("Card scanned detected")
    logger.warning("Initializing entering process")
    logger.warning("Sending request to CRM for card_scanned")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://crm_choreography:8002/card_scanned",
            json=card.reprJSON(),
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())


@app.post("/scan_again")
async def scan_again(user: User):
    logger.warning("Second scan request got")
    logger.warning("Enabling second scan")
    logger.warning("Waiting for the user to scan the card...")
    logger.warning("Second scan detected")
    card = Card(card_token="123abc123")
    logger.warning("Sending request to payments service to verify the card")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://payments_choreography:8006/verify_card",
            json=dict(user=user.reprJSON(), card=card.reprJSON()),
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
