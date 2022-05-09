import logging
import os
import time
from typing import Dict, List, Union

from shared.models import Product, User

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


def process_realize_payment_queue(
    time_to_sleep: int, PAYMENT_QUEUE: Dict[str, Union[List[Product], User]]
) -> None:
    while True:
        try:
            if PAYMENT_QUEUE["products"] and PAYMENT_QUEUE["customer"]:
                logger.warning("Obtained info about products and customer")
                logger.warning("Printing receipt...")
                logger.warning("Receipt printed")
                PAYMENT_QUEUE = {}
        except KeyError:
            pass
        time.sleep(time_to_sleep)
