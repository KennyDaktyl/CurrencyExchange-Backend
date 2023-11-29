from django.urls import path

from .views import currencies

urlpatterns = [path("", currencies, name="currencies")]
