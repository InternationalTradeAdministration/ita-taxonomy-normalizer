import datetime
import logging

import azure.functions as func

from .taxonomy_io import etl


def main(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.warning("The timer is past due!")

    logging.info("Loading taxonomy at %s", datetime.datetime.utcnow())
    etl()
