import json
import logging
import os

import httpx
import redis
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Card, User
from shared.utils import populate_users_data

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

app = FastAPI()
redis_crm = redis.Redis(host="redis_crm", port=6379)

populate_users_data(redis_crm)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/card_scanned")
async def card_scanned(card: Card):
    logger.warning("Obtained card_scanned with card_token: %s", card.card_token)
    logger.warning("Checking if user with card_token: %s exists", card.card_token)
    user = redis_crm.get(card.card_token)
    if not user:
        logger.warning("User not known, initializing registration process")
        logger.warning("Requesting registration form to be shown by the screen")
        async with httpx.AsyncClient() as client:
            await client.post(
                "http://screen_choreography:8009/registration_form",
                json={"card_token": card.card_token},
            )
    else:
        user_dict = json.loads(user)
        try:
            user_class_obj = User(
                card_token=user_dict["card_token"],
                name=user_dict["name"],
                surname=user_dict["surname"],
            )
        except KeyError:
            raise Exception("User found but entity unprocessable")
        logger.warning("User found. User data: %s", user_class_obj.reprJSON())
        await open_doors_and_finish_entering_process()
    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())


@app.post("/registration_form")
async def validate_registration_data(user: User):
    logger.warning("Obtained user registration data")
    logger.warning("Validating data...")
    logger.warning("Data validated successfully")
    logger.warning("Saving user in the database")
    user = redis_crm.set(name=user.card_token, value=json.dumps(user.reprJSON()))
    logger.warning("User data: %s", user.reprJSON())
    logger.warning("Requesting screen to show info about scanning card again")
    async with httpx.AsyncClient() as client:
        await client.get("http://screen_choreography:8009/scan_again")
    logger.warning("Requesting terminal for second scan")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://terminal_choreography:8010/scan_again", json=user.reprJSON()
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())


@app.post("/card_verified")
async def save_user(user: User):
    logger.warning("Obtained verified card with user data after second scan")
    logger.warning("Saving user in the database")
    user = redis_crm.set(name=user.card_token, value=json.dumps(user.reprJSON()))
    logger.warning("User data: %s", user.reprJSON())
    await open_doors_and_finish_entering_process()
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())


async def open_doors_and_finish_entering_process():
    logger.warning("Requesting screen to show entering doors info")
    async with httpx.AsyncClient() as client:
        await client.post("http://screen_choreography:8009/open_doors")
    logger.warning("Requesting doors to open")
    async with httpx.AsyncClient() as client:
        await client.get("http://doors_choreography:8003/open")
    return None
