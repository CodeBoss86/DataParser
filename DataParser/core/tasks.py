from DataParser.celery import app as celery_app
from .management.commands import app

import logging
logging.basicConfig(level=logging.INFO)
# Get an instance of a logger
logger = logging.getLogger(__name__)


@celery_app.task
def run_app():
    """
    Run app to pull data from feeds, parse and store to DB
    """
    try:
        command = app.Command()
        command.app()

    except Exception as e:
        logger.error(e)

