import logging
import os
import time
from typing import Dict, List, Union

import httpx
from shared.models import Product, User

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


async def process_generating_ereceipt_queue(
    time_to_sleep: int, ERECEIPT_GENERATING_QUEUE: Dict[str, Union[List[Product], User]]
) -> None:
    while True:
        try:
            if (
                ERECEIPT_GENERATING_QUEUE["products"]
                and ERECEIPT_GENERATING_QUEUE["customer"]
            ):
                logger.warning("Obtained info about products and customer")
                logger.warning("Generating e-receipt...")
                logger.warning("E-receipt generated")
                logger.warning(
                    "Requesting message service to send e-receipt to the customer"
                )
                async with httpx.AsyncClient() as client:
                    await client.post(
                        "http://messages_choreography:8005/send_ereceipt",
                        json=ERECEIPT_GENERATING_QUEUE["customer"].reprJSON(),  # type: ignore [union-attr]
                    )
                ERECEIPT_GENERATING_QUEUE = {}
        except KeyError:
            pass
        time.sleep(time_to_sleep)
