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


@app.post("/card_scanned", response_model=Card, status_code=status.HTTP_200_OK)
async def card_scanned(card: Card):
    logger.warning("Obtained card_scanned with card_token: %s", card.card_token)
    logger.warning("Checking if user with card_token: %s exists", card.card_token)
    user = redis_crm.get(card.card_token)
    if not user:
        logger.warning("User not known, initializing registration process")
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
        logger.warning("Requesting screen to show entering doors info")
        async with httpx.AsyncClient() as client:
            await client.post("http://screen_choreography:8009/open_doors")
        logger.warning("Requesting doors to open")
        async with httpx.AsyncClient() as client:
            await client.post("http://doors_choreography:8003/open")
    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())
