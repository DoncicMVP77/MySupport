import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
# app.conf.enable_utc = False
# app.conf.update(timezone='Europe/Moscow')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

#Celery Beat Settings
app.conf.beat_schedule = {
    'change_ticket_status': {
        'task': 'test_celery.tasks.check_last_message_in_ticket_and_send_email_about_change_status',
        'schedule': crontab(hour=0, minute=30),
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
