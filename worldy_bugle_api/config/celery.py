import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Schedule the task to run every hour
app.conf.beat_schedule = {
    "fetch-new-articles-every-hour": {
        "task": "apps.feeds.tasks.fetch_new_articles",
        "schedule": crontab(minute=0, hour="*"),
    },
}
