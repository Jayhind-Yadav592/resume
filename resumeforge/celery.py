import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resumeforge.settings')

app = Celery('resumeforge')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Periodic Tasks Configuration
app.conf.beat_schedule = {
    'send-weekly-pro-digest': {
        'task': 'resumes.tasks.send_weekly_pro_digest',
        # Runs every Monday at 9:00 AM UTC
        'schedule': crontab(hour=9, minute=0, day_of_week='monday'),
    },
}
