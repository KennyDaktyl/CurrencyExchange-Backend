import requests
import logging

from celery import shared_task
from celery.utils.log import get_task_logger

from rest_framework.exceptions import ValidationError

from .models import Currency
from .serializers import CurrencyRequestSerializer
from .utils import local_time_str, timezone

logger = logging.getLogger(__name__)

API_URL = "https://api.nbp.pl/api/exchangerates/tables/A/"
CURRENCIES_TO_UPDATE = ["EUR", "USD"]


@shared_task
def update_currency_rates():
    response = requests.get(API_URL)
    data = response.json()[0]["rates"]

    for currency_data in data:
        update_currency(currency_data)


def update_currency(currency_data):
    code = currency_data["code"]

    if code in CURRENCIES_TO_UPDATE:
        name = currency_data["currency"]
        rate = currency_data["mid"]

        serializer = create_serializer(name, code, rate)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            currency = update_or_create_currency(validated_data)

            logger.info(
                f"Uaktualniono kurs waluty: {currency.code} - {local_time_str()}"
            )
        else:
            logger.error(
                f"Błąd walidacji danych: {ValidationError(serializer.errors)}"
            )


def create_serializer(name, code, rate):
    return CurrencyRequestSerializer(
        data={"name": name, "code": code, "rate": rate}
    )


def update_or_create_currency(validated_data):
    currency, created = Currency.objects.update_or_create(
        name=validated_data["name"],
        code=validated_data["code"],
    )
    currency.rate = validated_data["rate"]
    currency.last_updated = timezone.now()
    currency.save()
    return currency
