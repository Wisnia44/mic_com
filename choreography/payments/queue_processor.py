import logging
import os
import time
from typing import Dict, List, Union

from shared.models import Product, User

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

PAYMENT_QUEUE: Dict[str, Union[List[Product], User]] = {}


def process_realize_payment_queue(time_to_sleep: int) -> None:
    while True:
        if PAYMENT_QUEUE["products"] and PAYMENT_QUEUE["customer"]:
            logger.warning("Obtained info about products and customer")
            logger.warning("Printing receipt...")
            logger.warning("Receipt printed")
            PAYMENT_QUEUE: Dict[str, Union[List[Product], User]] = {}
        elif PAYMENT_QUEUE["products"]:
            logger.warning("Waiting for info about customer to print the receipt...")
        elif PAYMENT_QUEUE["customer"]:
            logger.warning("Waiting for info about products to print the receipt...")
        time.sleep(time_to_sleep)
