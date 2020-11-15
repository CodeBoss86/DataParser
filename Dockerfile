
FROM python:3.8

RUN apt-get update
ENV PYTHONUNBUFFERED=1

COPY . /opt/DataParserToDB

WORKDIR /opt/DataParserToDB

RUN python3 -m pip install -r /opt/DataParserToDB/requirements.txt

WORKDIR /opt/DataParserToDB/DataParser

RUN mkdir /opt/DataParserToDB/DataParser/data

VOLUME ["/opt/DataParserToDB/DataParser/data"]

