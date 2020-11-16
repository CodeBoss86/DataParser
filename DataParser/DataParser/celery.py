import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataParser.settings')

app = Celery('DataParser', backend='redis://localhost', broker='pyamqp://')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['core'])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
