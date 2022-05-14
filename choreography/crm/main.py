import json
import logging
import os

import httpx
import redis
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Card, User
from shared.utils import populate_users_data, user1

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

app = FastAPI()
redis_crm = redis.Redis(host="redis_crm_choreography", port=6379)

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
                address=user_dict["address"],
            )
        except KeyError:
            raise Exception("User found but entity unprocessable")
        logger.warning("User found. User data: %s", user_class_obj.reprJSON())
        await open_doors_and_finish_entering_process()
    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())


@app.post("/registration_data")
async def validate_registration_data(user: User):
    logger.warning("Obtained user registration data")
    logger.warning("Validating data...")
    logger.warning("Data validated successfully")
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
    redis_crm.set(name=user.card_token, value=json.dumps(user.reprJSON()))
    logger.warning("User saved. User data: %s", user.reprJSON())
    await open_doors_and_finish_entering_process()
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())


@app.get("/customer_info")
async def get_customer_info_on_checkout():
    logger.warning("Obtained request to get customer info on checkout")
    logger.warning("Getting user from the database")
    user = user1
    logger.warning("User data: %s", user.reprJSON())
    logger.warning("Requesting receipt service to print receipt")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://receipt_choreography:8008/customer_info", json=user.reprJSON()
        )
    logger.warning("Requesting e-receipt service to generate e-receipt")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://ereceipt_choreography:8004/customer_info", json=user.reprJSON()
        )
    logger.warning("Requesting payment service to realize payment")
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://payments_choreography:8006/customer_info", json=user.reprJSON()
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())


async def open_doors_and_finish_entering_process():
    logger.warning("Requesting screen to show entering doors info")
    async with httpx.AsyncClient() as client:
        await client.get("http://screen_choreography:8009/open_doors")
    logger.warning("Requesting doors to open")
    async with httpx.AsyncClient() as client:
        await client.get("http://doors_choreography:8003/open")
    return None
