import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricecalc.settings')

app = Celery('pricecalc')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() 

# app.conf.beat_schedule = {
#     'update-data-every-1-minute': {
#         'task': 'calc.tasks.update_data_regularly',
#         'schedule': crontab(minute='*/1'),
#     }
# }
