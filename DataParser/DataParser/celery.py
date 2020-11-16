import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataParser.settings')

app = Celery('DataParser')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['core'])

app.conf.beat_schedule = {
    'execute-data-parser-task': {
        'task': 'tasks.run_app',
        'schedule': crontab(minute='*/5')
    },
}

app.conf.timezone = 'UTC'