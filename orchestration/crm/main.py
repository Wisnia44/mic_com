import json
import logging
import os

import redis
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import User
from shared.utils import populate_users_data

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

app = FastAPI()
redis_crm = redis.Redis(host="redis_crm_orchestration", port=6379)

populate_users_data(redis_crm)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


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
