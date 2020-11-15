from django.core.management.base import BaseCommand

import time
import asyncio

import logging

logging.basicConfig(level=logging.INFO)
# Get an instance of a logger
logger = logging.getLogger(__name__)

from core.parser import download_from_feeds, data_processor


class Command(BaseCommand):
    help = "Parse data feeds and store to DB"

    def app(self):
        logger.info("app started")

        price_feeds = [
            "http://recruitment-75b8.kxcdn.com/one.csv.gz", 
            "http://recruitment-75b8.kxcdn.com/two.csv.gz", 
            "http://recruitment-75b8.kxcdn.com/three.csv.gz", 
            "http://recruitment-75b8.kxcdn.com/1.xml.gz", 
            "http://recruitment-75b8.kxcdn.com/2.xml.gz", 
            "http://recruitment-75b8.kxcdn.com/3.xml.gz"
        ]

        data_columns = ["ident", "store_id", "previous_price", 
                "price", "currency", "offer_description", 
                "manufacturersku", "eankod", "additional_info", 
                "producturl", "stockstatus"]

        start_time1 = time.time()
        asyncio.run(download_from_feeds(price_feeds))

        file_names = [url.split('.com/')[1][:-3] for url in price_feeds]
        asyncio.run(data_processor(file_names))

        duration1 = time.time() - start_time1
        logger.info(f"Duration1 {duration1} seconds")


    def handle(self, *args, **kwargs):
        self.app()