import logging
import os
from typing import List

import httpx
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from shared.models import Product, User

router = APIRouter()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@router.get("/checkout")
async def checkout():
    logger.warning(
        "Doors opened, customer left the store, initializing checkout process"
    )
    customer = await _get_customer_data()
    products = await _get_products_data()
    products_with_prices = await _get_prices_for_products(products)
    await _print_receipt(products_with_prices)
    ereceipt = await _generate_ereceipt(products_with_prices)
    await _send_ereceipt(ereceipt, customer)
    await _realize_payment()
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


async def _get_customer_data() -> User:
    logger.warning("Calling CRM to get info about customer")
    async with httpx.AsyncClient() as client:
        response = await client.get("http://crm_choreography:8002/customer_info")
    logger.warning("Response from CRM: %s", response.text)
    user_data = response.json()
    return User(
        card_token=user_data["card_token"],
        name=user_data["name"],
        surname=user_data["surname"],
        address=user_data["address"],
    )


async def _get_products_data() -> List[Product]:
    logger.warning("Calling AI to get info about purchased products")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://ai_choreography:8001/get_purchased_products"
        )
    logger.warning("Response from AI: %s", response.text)
    products = []
    for product in response.json():
        products.append(
            Product(
                name=product["name"],
                price=product["price"],
                quantity=product["quantity"],
            )
        )
    return products


async def _get_prices_for_products(products: List[Product]) -> List[Product]:
    products_json = [product.reprJSON() for product in products]
    logger.warning("Request PIM to get products prices")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://pim_choreography:8007/get_prices", json=products_json
        )
    logger.warning("Response from PIM: %s", response.text)
    products = []
    for product in response.json():
        products.append(
            Product(
                name=product["name"],
                price=product["price"],
                quantity=product["quantity"],
            )
        )
    return products


async def _print_receipt(products: List[Product], customer: User) -> None:
    products_json = [product.reprJSON() for product in products]
    logger.warning("Requesting receipt service to print receipt")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://receipt_orchestration:8008/print_receipt",
            json=dict(products=products_json, customer=customer.reprJSON()),
        )
    logger.warning("Response from receipt: %s", response.text)
    return None


async def _generate_ereceipt(products: List[Product], customer: User) -> bytes:
    products_json = [product.reprJSON() for product in products]
    logger.warning("Requesting e-receipt service to generate e-receipt")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://ereceipt_orchestration:8004/generate_ereceipt",
            json=dict(products=products_json, customer=customer.reprJSON()),
        )
    logger.warning("Response from e-receipt: %s", response.text)
    return response.json()["ereceipt"]


async def _send_ereceipt(ereceipt: bytes, customer: User) -> None:
    logger.warning("Requesting message service to send e-receipt to the customer")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://messages_orchestration:8005/send_ereceipt",
            json=dict(ereceipt=ereceipt, customer=customer.reprJSON()),
        )
    logger.warning("Response from messages: %s", response.text)
    return None


async def _realize_payment():
    logger.warning("Requesting payments service to realize payment")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://payments_orchestration:8006/realize_payment"
        )
    logger.warning("Response from payments: %s", response.text)
    return None
