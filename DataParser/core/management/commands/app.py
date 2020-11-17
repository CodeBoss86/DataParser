from django.core.management.base import BaseCommand

import time
import asyncio
import schedule
import logging

logging.basicConfig(level=logging.INFO)
# Get an instance of a logger
logger = logging.getLogger(__name__)

from core.parser import download_from_feeds, data_parser, data_processor


def app():
    logger.info("app started")

    price_feeds = [
        "http://recruitment-75b8.kxcdn.com/one.csv.gz", 
        "http://recruitment-75b8.kxcdn.com/two.csv.gz", 
        "http://recruitment-75b8.kxcdn.com/three.csv.gz", 
        "http://recruitment-75b8.kxcdn.com/1.xml.gz", 
        "http://recruitment-75b8.kxcdn.com/2.xml.gz", 
        "http://recruitment-75b8.kxcdn.com/3.xml.gz"
    ]

    start_time = time.time()
    
    # asynchronousy download product data from source
    asyncio.run(download_from_feeds(price_feeds))

    # extract filenames into list
    file_names = [url.split('.com/')[1][:-3] for url in price_feeds]
    print(file_names)

    asynchronously parse downloaded data
    parsed_data = asyncio.run(data_parser(file_names))

    multi process data to DB
    data_processor(parsed_data)

    duration = time.time() - start_time
    logger.info(f"Duration {duration} seconds")


# schedule for periodic run
schedule.every(3).minutes.do(app)


class Command(BaseCommand):
    help = "Parse data feeds and store to DB"

    def handle(self, *args, **kwargs):
        #execute app and run periodically
        app()
        while True:
            schedule.run_pending()
            time.sleep(1)

