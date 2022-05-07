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


@app.post("/card_scanned", response_model=Card)
async def card_scanned(card: Card):
    logger.warning("Card scanned detected")
    logger.warning("Initializing entering process")
    logger.warning("Sending request to CRM for card_scanned")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://crm_choreography:8002/card_scanned",
            json={"card_token": card.card_token},
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())
