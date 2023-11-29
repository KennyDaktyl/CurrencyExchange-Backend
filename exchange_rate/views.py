from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Currency
from .serializers import CurrencyResponseSerializer


class CurrencyRatesView(APIView):
    renderer_classes = [JSONRenderer]

    @method_decorator(cache_page(15))
    def get(self, request):
        currencies = Currency.objects.filter(is_active=True)
        serializer = CurrencyResponseSerializer(currencies, many=True)
        return Response(serializer.data)


currencies = CurrencyRatesView.as_view()
