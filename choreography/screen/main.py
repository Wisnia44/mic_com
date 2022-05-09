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


@app.get("/open_doors")
async def info_open_doors():
    logger.warning("Info about opening doors show request obtained")
    logger.warning("Showing info about opening doors...")
    logger.warning("Info shown")
    return JSONResponse(status_code=status.HTTP_200_OK)


@app.get("/scan_again")
async def info_scan_again():
    logger.warning("Info about second card scanning show request obtained")
    logger.warning("Showing info about scanning card again...")
    logger.warning("Info shown")
    return JSONResponse(status_code=status.HTTP_200_OK)


@app.post("/registration_form")
async def show_registration_form(card: Card):
    logger.warning("Requested to show registration form")
    logger.warning("Requested form shown")
    logger.warning("Gathering data from the user...")
    logger.warning("Sending gathered data to CRM")
    data = User(card_token=card.card_token, name="Harry", surname="Kane")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://crm_choreography:8002/registration_data", json=data.reprJSON()
        )
    return JSONResponse(status.HTTP_200_OK)
