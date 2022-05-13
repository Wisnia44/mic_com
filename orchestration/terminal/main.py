import logging
import os

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Card

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.get("/scan_again")
async def scan_again():
    logger.warning("Second scan request got")
    logger.warning("Enabling second scan")
    logger.warning("Waiting for the user to scan the card...")
    logger.warning("Second scan detected")
    card = Card(card_token="123abc123")
    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())


@app.post("/card_scanned")
async def card_scanned(card: Card):
    logger.warning("Card scanned detected")
    logger.warning("Initializing entering process")
    logger.warning("Notifying orchestrator")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://orchestrator_orchestration:8000/entering",
            json=card.reprJSON(),
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())
