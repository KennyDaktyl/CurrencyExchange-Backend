from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CurrencyExchange.settings")

app = Celery("CurrencyExchange")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "update-currency-rates": {
        "task": "exchange_rate.tasks.update_currency_rates",
        "schedule": crontab(minute="*/1"),
    },
}

app.autodiscover_tasks()
