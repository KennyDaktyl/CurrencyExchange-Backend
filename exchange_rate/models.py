from django.db import models
from django.utils import timezone


class Currency(models.Model):
    last_updated = models.DateTimeField(default=timezone.now)
    name = models.CharField(verbose_name="Nazwa waluty", max_length=128)
    code = models.CharField(
        verbose_name="Kod waluty", max_length=8, db_index=True
    )
    rate = models.DecimalField(
        verbose_name="Kurs waluty", decimal_places=10, max_digits=20, default=0
    )
    is_active = models.BooleanField(verbose_name="Czy aktywna", default=True)

    class Meta:
        ordering = ("code",)
        verbose_name_plural = "Kursy walut"

    def save(self, *args, **kwargs):
        if self.rate is not None:
            self.rate = "{0:f}".format(self.rate).rstrip("0")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"""Kurs waluty {self.code}: {self.rate}\n
            - Aktualizacja z {self.last_updated}"""
