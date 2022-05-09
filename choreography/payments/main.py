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


@app.post("/verify_card")
async def verify_card(card: Card, user: User):
    logger.warning("Card verification request got")
    logger.warning("Verifying card...")
    logger.warning("Card verification successfull")
    logger.warning("Sending request to CRM with successfully verified card")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://crm_choreography:8002/card_verified",
            json=user.reprJSON(),
        )
    return JSONResponse(status_code=status.HTTP_200_OK)
