import logging
import os

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.models import Ereceipt, User

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {}


@app.post("/send_ereceipt")
async def send_ereceipt(customer: User, ereceipt: Ereceipt):
    logger.warning(
        "Obtained request to send e-receipt to the user to the address: %s",
        customer.address,
    )
    logger.warning("Obtained e-receipt to send: %s", ereceipt)
    logger.warning("Sending...")
    logger.warning("E-receipt sent")
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
