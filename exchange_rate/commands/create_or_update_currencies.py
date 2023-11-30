import logging

from rest_framework.exceptions import ValidationError

from exchange_rate.models import Currency
from exchange_rate.serializers import CurrencyRequestSerializer
from exchange_rate.utils import local_time_str, timezone

logger = logging.getLogger(__name__)


CURRENCIES_TO_UPDATE = ["EUR", "USD"]


def update_currency(currency_data):
    code = currency_data["code"]

    if code in CURRENCIES_TO_UPDATE:
        name = currency_data["currency"]
        rate = currency_data["mid"]

        serializer = CurrencyRequestSerializer(
            data={"name": name, "code": code, "rate": rate}
        )

        if serializer.is_valid():
            validated_data = serializer.validated_data
            currency = update_or_create_currency(validated_data)

            logger.info(
                f"Uaktualniono kurs: {currency.code} - {local_time_str()}"
            )
        else:
            logger.error(
                f"Błąd walidacji danych: {ValidationError(serializer.errors)}"
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
