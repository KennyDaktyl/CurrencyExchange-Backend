from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.utils import timezone

from exchange_rate.models import Currency
from exchange_rate.serializers import CurrencyRequestSerializer
from exchange_rate.tasks import update_currency_rates


class UpdateCurrencyRatesTestCase(TestCase):
    data = [
        {
            "table": "A",
            "no": "231/A/NBP/2023",
            "effectiveDate": "2023-11-29",
            "rates": [
                {"currency": "funt szterling", "code": "GBP", "mid": 5.0066},
                {
                    "currency": "dolar amerykański",
                    "code": "USD",
                    "mid": 3.9478,
                },
                {"currency": "euro", "code": "EUR", "mid": 4.3327},
                {"currency": "dolar Hongkongu", "code": "HKD", "mid": 0.5060},
                {"currency": "dolar kanadyjski", "code": "CAD", "mid": 2.9078},
            ],
        }
    ]

    @patch("exchange_rate.tasks.requests.get")
    def test_update_currency_rates(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.data
        mock_requests_get.return_value = mock_response

        update_currency_rates()

        currencies = Currency.objects.filter(code__in=["EUR", "USD"])
        self.assertEqual(currencies.count(), 2)

        for currency in currencies:
            self.assertTrue(currency.rate > 0)
            self.assertTrue(
                currency.last_updated
                > timezone.now() - timezone.timedelta(minutes=1)
            )

    def test_serializer_valid_data(self):
        data = {"code": "EUR", "name": "Euro", "rate": 4.1234}
        serializer = CurrencyRequestSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["name"], "Euro")
        self.assertEqual(validated_data["code"], "EUR")
        self.assertAlmostEqual(validated_data["rate"], Decimal(4.1234000000))

    def test_serializer_invalid_data(self):
        data = {"brak_code": "PLN", "name": None, "rate": "jakies złe dane"}
        serializer = CurrencyRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        self.assertIn("rate", errors)

    def test_serializer_large_decimal(self):
        data = {"code": "PLN", "name": "Polski złoty", "rate": 5.1234567891011}
        serializer = CurrencyRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())
