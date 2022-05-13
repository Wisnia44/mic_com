import logging
import os
from typing import Optional

import httpx
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from registration import registration
from shared.models import Card, User

router = APIRouter()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@router.post("/entering")
async def entering(card: Card):
    logger.warning("Card scanned, initializing entering process")
    user = await _get_user(card)
    if not user:
        successfull_registration = await registration(card)
        if not successfull_registration:
            logger.error("Registration finished unsuccessfully, exiting...")
            JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})
    await _open_door()
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


async def _get_user(card: Card) -> Optional[User]:
    logger.warning("Sending request to CRM for card_scanned")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://crm_orchestration:8002/get_user",
            json=card.reprJSON(),
        )
    logger.warning("Obtained response from CRM: %s", response.text)
    try:
        user_data = response.json()
        return User(
            card_token=user_data["card_token"],
            name=user_data["name"],
            surname=user_data["surname"],
            address=user_data["address"],
        )
    except KeyError:
        return None


async def _open_door() -> None:
    logger.warning("Requesting screen to show info about opening door")
    async with httpx.AsyncClient() as client:
        response_screen = await client.get(
            "http://screen_orchestration:8009/open_doors"
        )
    logger.warning("Obtained response from screen: %s", response_screen.text)

    logger.warning("Requesting doors to open")
    async with httpx.AsyncClient() as client:
        response_door = await client.get("http://doors_orchestration:8003/open")
    logger.warning("Obtained response from door: %s", response_door.text)

    return None
