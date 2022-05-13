import json
import logging
import os

import httpx
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from shared.models import Card, User

router = APIRouter()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@router.post("/new_user")
async def card_scanned(card: Card):
    logger.warning("User not known, initializing registration process")

    registration_data = await _registration_form(card)
    successfull_validation = await _data_validation(registration_data)
    if successfull_validation:
        second_card_data = await _second_card_scan()
        card_verification = await _verify_card(second_card_data)
        if card_verification:
            await _save_user(registration_data)
            await _open_door()
        else:
            logger.error("Card verification failed, exiting...")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        logger.error("Data validation failed, exiting...")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JSONResponse(status_code=status.HTTP_200_OK, content=card.reprJSON())


async def _registration_form(card: Card) -> User:
    logger.warning("Requesting registration form to be shown by the screen")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://screen_orchestration:8009/registration_form", json=card.reprJSON()
        )
    logger.warning("Obtained response from screen: %s", response.text)
    registration_data = User.dict_init(json.loads(response.json()))
    return registration_data


async def _data_validation(user_data: User) -> bool:
    logger.warning("Requesting CRM to validate the data...")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://crm_orchestration:8002/validate_data", json=user_data.reprJSON()
        )
    logger.warning("Obtained response from CRM: %s", response.text)
    if response.status_code == status.HTTP_200_OK:
        return True
    else:
        return False


async def _second_card_scan() -> Card:
    logger.warning("Requesting screen to show info about scanning card again")
    async with httpx.AsyncClient() as client:
        response_screen = await client.get(
            "http://screen_orchestration:8009/scan_again"
        )
    logger.warning("Obtained response from screen: %s", response_screen.text)

    logger.warning("Requesting terminal for second scan")
    async with httpx.AsyncClient() as client:
        response_terminal = await client.post(
            "http://terminal_orchestration:8010/scan_again"
        )
    logger.warning("Obtained response from terminal: %s", response_terminal.text)

    second_card_data = Card(
        card_token=json.loads(response_terminal.json())["card_token"]
    )
    return second_card_data


async def _verify_card(card: Card) -> bool:
    logger.warning("Sending request to payments service to verify the card")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://payments_orchestration:8006/verify_card", json=card.reprJSON()
        )
    logger.warning("Obtained response from payments: %s", response.text)
    if response.status_code == status.HTTP_200_OK:
        return True
    else:
        return False


async def _save_user(user: User) -> None:
    logger.warning("Sending request to CRM to save the user")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://crm_choreography:8002/save_user",
            json=user.reprJSON(),
        )
    logger.warning("Obtained response from CRM: %s", response.text)
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
