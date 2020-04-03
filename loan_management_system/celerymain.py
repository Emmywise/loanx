import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_management_system.settings')

app = Celery('loan_management_system')
#app = Celery('loan_management_system', backend='rpc://', broker='pyamqp://')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()