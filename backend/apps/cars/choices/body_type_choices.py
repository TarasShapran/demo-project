from django.db import models


class BodyTypeChoices(models.TextChoices):
    Hatchback = 'Hatchback',
    Sedan = 'Sedan',
    Coupe = 'Coupe',
    Jeep = 'Jeep'


class CurrencyTypeChoices(models.TextChoices):
    EUR = 'EUR',
    UAH = 'UAH',
    USD = 'USD'


class CurrencyTypeISOChoices(models.TextChoices):
    EUR = 978,
    UAH = 980,
    USD = 840

