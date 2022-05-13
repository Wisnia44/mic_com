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


@app.get("/open_doors")
async def info_open_doors():
    logger.warning("Info about opening doors show request obtained")
    logger.warning("Showing info about opening doors...")
    logger.warning("Info shown")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.get("/scan_again")
async def info_scan_again():
    logger.warning("Info about second card scanning show request obtained")
    logger.warning("Showing info about scanning card again...")
    logger.warning("Info shown")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


@app.post("/registration_form")
async def show_registration_form(card: Card):
    logger.warning("Requested to show registration form")
    logger.warning("Requested form shown")
    logger.warning("Gathering data from the user...")
    user_data = User(
        card_token=card.card_token,
        name="Harry",
        surname="Kane",
        address="harry.kane@email.com",
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=user_data.reprJSON())
