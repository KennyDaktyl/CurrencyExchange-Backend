from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from exchange_rate.models import Currency


class CurrencyRatesViewTestCase(TestCase):
    def setUp(self):
        Currency.objects.create(
            name="Euro",
            code="EUR",
            rate=4.3327,
            last_updated="2023-11-30 12:00:00",
            is_active=True,
        )
        Currency.objects.create(
            name="Dolar amerykański",
            code="USD",
            rate=3.9478,
            last_updated="2023-11-30 12:00:00",
            is_active=True,
        )

    def test_currency_rates_view(self):
        client = Client()
        response = client.get(reverse("currencies"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "name": "Euro",
                "code": "EUR",
                "rate": 4.3327,
                "last_updated": "2023-11-30 12:00:00",
            },
            {
                "name": "Dolar amerykański",
                "code": "USD",
                "rate": 3.9478,
                "last_updated": "2023-11-30 12:00:00",
            },
        ]
        self.assertEqual(response.json(), expected_data)
