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
redis_crm = redis.Redis(host="redis_crm", port=6379)

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
