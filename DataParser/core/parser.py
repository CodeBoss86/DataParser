import time
import asyncio
import pandas as pd
import xml.etree.ElementTree as ET
from smart_open import open as smartOpen
from core.models import ProductData
from django.db import DatabaseError, transaction

import logging
logging.basicConfig(level=logging.INFO)
# Get an instance of a logger
logger = logging.getLogger(__name__)


async def parse_xml(file):
    """
    Parse the XML file and return its data
    """

    logger.info("About to parse xml file")

    xml_file = open(file, 'rb')
    # represent the xml file as a tree
    tree = ET.parse(xml_file)
    root = tree.getroot()       # grab the root containing the nodes

    products_data = list()
    for node in root:
        data = dict()
        for element in data_columns:
            value = node.find(element).text
            data[element] = value
        products_data.append(ProductData(**data))

    return products_data


async def parse_csv(file):
    """
    Parse the CSV file and return its data
    """
    logger.info("About to parse xml file")
    
    # read csv file into pandas dataframe
    dataframe = pd.read_csv(file, low_memory=False)
    # rename columns
    dataframe = dataframe.rename(str.strip, axis='columns')
    # convert dataframe to python object 
    df_to_dict = dataframe.to_dict('records')

    products_data = [ProductData(**data) for data in df_to_dict]

    return products_data


async def commit_to_DB(data):
    """
    Save data to DB
    """
    logger.info("Commiting data to DB")
    
    try:
        with transaction.atomic():
            ProductData.objects.bulk_create(data)
            return True
    except DatabaseError as err:
        logger.error(err)
        return False


async def fetch_file_from_url(url):
    """
    Download file from URL to local directory
    """
    logger.info("Downloading file from URL to local directory data")
    
    file_name = url.split('.com/')[1][:-3]

    with smartOpen(url, 'rb') as downloaded_file:
        with open(file_name, 'wb') as local_file:
            for line in downloaded_file:
                local_file.write(line)
    
    logger.info(f"FETCH :: {file_name} :: COMPLETE")


async def download_from_feeds(urls):
    logger.info("Downloading data from URL feeds")
    
    async_tasks = list()
    for url in urls:
        task = asyncio.create_task(fetch_file_from_url(url))
        async_tasks.append(task)

        await asyncio.gather(*async_tasks, return_exceptions=True)


async def parse_data(file):
    async_tasks = list()

    if file.endswith('.csv'):
        task = asyncio.create_task(parse_csv(file))

    elif file.endswith('.xml'):
        task = asyncio.create_task(parse_xml(file))

    async_tasks.append(task)
    await asyncio.gather(*async_tasks, return_exceptions=True)


async def data_processor(files):
    logger.info("processing data")
    for file in files:

        data = await parse_data(file)
        # store data to DB
        await commit_to_DB(data)

    logger.info("Process Finished")


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

    data_columns = ["ident", "store_id", "previous_price", 
            "price", "currency", "offer_description", 
            "manufacturersku", "eankod", "additional_info", 
            "producturl", "stockstatus"]

    start_time1 = time.time()
    asyncio.run(download_from_feeds(price_feeds))

    file_names = [url.split('.com/')[1][:-3] for url in price_feeds]
    asyncio.run(data_processor(file_names))

    duration1 = time.time() - start_time1
    print(f"Duration1 {duration1} seconds")


if __name__ == "__main__":
    app()
