import logging
import os
import time
from typing import Dict, List, Union

from shared.models import Product, User

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))


def process_receipt_printing_queue(
    time_to_sleep: int, PRINTING_QUEUE: Dict[str, Union[List[Product], User]]
) -> None:
    while True:
        try:
            if PRINTING_QUEUE["products"] and PRINTING_QUEUE["customer"]:
                logger.warning("Obtained info about products and customer")
                logger.warning("Printing receipt...")
                logger.warning("Receipt printed")
                PRINTING_QUEUE = {}
        except KeyError:
            pass
        time.sleep(time_to_sleep)
