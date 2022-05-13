import json
import logging
import os

import redis
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Card, User
from shared.utils import populate_users_data, user1

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

app = FastAPI()
redis_crm = redis.Redis(host="redis_crm_orchestration", port=6379)

populate_users_data(redis_crm)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/get_user")
async def get_user(card: Card):
    logger.warning("Obtained get_user request for a card: %s", card.reprJSON())
    logger.warning("Getting user from the database...")
    user_db = redis_crm.get(card.card_token)
    if not user_db:
        logger.warning("User not known, returning None...")
        return JSONResponse(status_code=status.HTTP_200_OK, content={})
    else:
        user_dict = json.loads(user_db)
        try:
            user = User(
                card_token=user_dict["card_token"],
                name=user_dict["name"],
                surname=user_dict["surname"],
                address=user_dict["address"],
            )
        except KeyError:
            raise Exception("User found but entity unprocessable")
        logger.warning("User found. User data: %s", user.reprJSON())
        return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())


@app.post("/validate_data")
async def validate_registration_data(user: User):
    logger.warning("Obtained user registration data")
    logger.warning("Validating data...")
    logger.warning("Data validated successfully")
    logger.warning("User data: %s", user.reprJSON())
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())


@app.post("/save_user")
async def save_user(user: User):
    logger.warning("Obtained verified card with user data after second scan")
    logger.warning("Saving user in the database")
    redis_crm.set(name=user.card_token, value=json.dumps(user.reprJSON()))
    logger.warning("User saved. User data: %s", user.reprJSON())
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())


@app.get("/customer_info")
async def get_customer_info_on_checkout():
    logger.warning("Obtained request to get customer info on checkout")
    logger.warning("Getting user from the database")
    user = user1
    logger.warning("User data: %s", user.reprJSON())
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.reprJSON())
