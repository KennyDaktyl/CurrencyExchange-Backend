from django.contrib import admin

from exchange_rate.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "rate", "is_active")
    list_filter = ("code", "is_active")
    search_fields = ("name", "code")
