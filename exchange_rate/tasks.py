import requests
from celery import shared_task

from .commands.create_or_update_currencies import update_currency

API_URL = "https://api.nbp.pl/api/exchangerates/tables/A/"


@shared_task
def update_currency_rates():
    response = requests.get(API_URL)
    data = response.json()[0]["rates"]

    for currency_data in data:
        update_currency(currency_data)
