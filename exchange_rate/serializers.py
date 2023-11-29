from rest_framework import serializers

from .models import Currency


class CurrencyRequestSerializer(serializers.ModelSerializer):
    rate = serializers.DecimalField(
        max_digits=20,
        decimal_places=10,
        coerce_to_string=False,
        required=False,
    )

    class Meta:
        model = Currency
        fields = [
            "name",
            "code",
            "rate",
        ]


class CurrencyResponseSerializer(serializers.ModelSerializer):
    last_updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    rate = serializers.DecimalField(
        max_digits=20,
        decimal_places=10,
        coerce_to_string=False,
    )

    class Meta:
        model = Currency
        fields = [
            "last_updated",
            "name",
            "code",
            "rate",
        ]
