from core.models import BaseModel

from django.db import models

from apps.cars.choices.body_type_choices import CurrencyTypeChoices


# Create your models here.
class ExchangeRateModel(BaseModel):
    class Meta:
        db_table = 'exchange_rate'
        ordering = ['id']

    ccy = models.CharField(max_length=3, choices=CurrencyTypeChoices.choices)  # USD, EUR, UAH
    base_ccy = models.CharField(max_length=3, choices=CurrencyTypeChoices.choices)  # USD, EUR, UAH
    buy = models.DecimalField(max_digits=15, decimal_places=5)
    sale = models.DecimalField(max_digits=15, decimal_places=5)
