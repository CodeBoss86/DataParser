from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    help = "Django command to pause execution until database is available"

    def handle(self, *args, **kwargs):
        self.stdout.write('waiting for database ...')
        db_conn = None
        while not db_conn:
            try:
                time.sleep(5)
                # get the database with keyword 'default' from settings.py
                db_conn = connections['default']
                # prints success messge in green
                self.stdout.write(self.style.SUCCESS('Database available :)'))
                time.sleep(2)
            except OperationalError:
                self.stdout.write("Database unavailable :(, waiting 2 second ...")
                time.sleep(2)
