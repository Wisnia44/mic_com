import logging
import os
import time
from typing import Dict, List, Union

from shared.models import Product, User

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

PRINTING_QUEUE: Dict[str, Union[List[Product], User]] = {}


def process_receipt_printing_queue(time_to_sleep: int) -> None:
    while True:
        if PRINTING_QUEUE["products"] and PRINTING_QUEUE["customer"]:
            logger.warning("Obtained info about products and customer")
            logger.warning("Printing receipt...")
            logger.warning("Receipt printed")
            PRINTING_QUEUE: Dict[str, Union[List[Product], User]] = {}
        elif PRINTING_QUEUE["products"]:
            logger.warning("Waiting for info about customer to print the receipt...")
        elif PRINTING_QUEUE["customer"]:
            logger.warning("Waiting for info about products to print the receipt...")
        time.sleep(time_to_sleep)
