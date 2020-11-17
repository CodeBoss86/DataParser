# DATAPARSER_TO_DB

DataParser_To_DB is a python appliation that downloads files in CSV and XML format from URL feeds, parses the downloaded files by fetching the information contained therein and stores the data retrieved in a database.

## How does it works?

It works by seamlessly connecting the magento webshop to user's accounting program through REST API endpoints provided to communicate with both the shop platform and accounting software. The application has been scheduled to pull data from magento API on an hourly basis and synchronize/push to Fortnox.

## Prerequisites
- Install the latest version of [Python3](https://www.python.org/downloads/)
- Install the latest version of [Docker-Engine](https://docs.docker.com/engine/install/)
- Install the latest version of [Docker-Compose](https://docs.docker.com/compose/install/)

## Installation & Setup
- Extract the contents of the Compressed-Archive file to current directory or folder of choice
- Navigate to the extracted folder/directory on terminal
```bash
cd DataParserToDB
```
- Ensure you are in the directory by listing its content
```bash
ls
```
Output should be similar to the following:
```bash
DataParser
docker-compose.yml
Dockerfile
LICENSE
README.md
requirements.txt
start.sh
```
- In the current directory, run the shell script to execute the program
```bash
sh start.sh
```


## Authors
- CodeMask.

