import os
import time
import multiprocessing
import asyncio
import pandas as pd
import xml.etree.ElementTree as ET
from smart_open import open as smartOpen
from core.models import ProductData
from django.db import DatabaseError, transaction
from asgiref.sync import sync_to_async

import logging
logging.basicConfig(level=logging.INFO)
# Get an instance of a logger
logger = logging.getLogger(__name__)

# set start method for multiprocessing
multiprocessing.set_start_method('fork')


data_columns = ["ident", "store_id", "previous_price", 
        "price", "currency", "offer_description", 
        "manufacturersku", "eankod", "additional_info", 
        "producturl", "stockstatus"]


async def parse_xml(file):
    """
    Parse the XML file and return its data
    """

    logger.info(f"parsing xml file :: {file}")

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
    
    # remove file to free up memory space
    os.remove(file)

    return products_data


async def parse_csv(file):
    """
    Parse the CSV file and return its data
    """
    logger.info(f"parsing csv file :: {file}")
    
    # read csv file into pandas dataframe
    dataframe = pd.read_csv(file, low_memory=False)
    # rename columns
    dataframe = dataframe.rename(str.strip, axis='columns')
    # convert dataframe to python object 
    df_to_dict = dataframe.to_dict('records')

    products_data = [ProductData(**data) for data in df_to_dict]

    # remove file to free up memory space
    os.remove(file)

    return products_data


def commit_to_DB(data):
    """
    Save data to DB
    """

    logger.info("Commiting data to DB")
    try:
        with transaction.atomic(): 
            ProductData.objects.bulk_create(data, ignore_conflicts=True)
            return True
    except DatabaseError as err:
        logger.error(err)
        return False


async def fetch_file_from_url(url):
    """
    Download file from URL to local directory
    """
    
    file_name = url.split('.com/')[1][:-3]
    logger.info(f"Downloading file :{file_name}: from URL to local directory data")

    with smartOpen(url, 'rb') as downloaded_file:
        with open(file_name, 'wb') as local_file:
            for line in downloaded_file:
                local_file.write(line)
    
    logger.info(f"FETCH :: {file_name} :: COMPLETE")


async def download_from_feeds(urls):
    """
    Download data from URL feeds
    """
    
    async_tasks = list()
    for url in urls:
        logger.info(f"Downloading data from URL :{url}:")
        task = asyncio.create_task(fetch_file_from_url(url))
        async_tasks.append(task)

        await asyncio.gather(*async_tasks, return_exceptions=True)


async def data_parser(files):
    """
    Parse files holding data
    """
    logger.info("processing downloaded files")
    parsed_data = list()

    for file in files:

        if file.endswith('.csv'):
            task = asyncio.create_task(parse_csv(file))

        elif file.endswith('.xml'):
            task = asyncio.create_task(parse_xml(file))

        # Wait for 1 second
        await asyncio.sleep(1)

        # check if async task is done
        task_has_executed = False
        while not task_has_executed:
            task_has_executed = task.done()
            try:
                if task_has_executed:
                    data = task.result()

            except Exception as e:
                logger.error(e)
                await asyncio.sleep(1)

        parsed_data.append(data)
    
    return parsed_data


def data_processor(data):
    """
    Process the data to DB
    """

    with multiprocessing.Pool() as pool:
        pool.map(commit_to_DB, data)

    logger.info("Process Finished")

