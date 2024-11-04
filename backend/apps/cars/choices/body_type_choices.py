from django.db import models


class BodyTypeChoices(models.TextChoices):
    Hatchback = 'Hatchback',
    Sedan = 'Sedan',
    Coupe = 'Coupe',
    Jeep = 'Jeep'

class Region_Choiceas(models.TextChoices):
    Volyn = 'Volyn',
    Lviv = 'Lviv',
    Rivne = 'Rivne',
    Kyiv = 'Kyiv'


class CurrencyTypeChoices(models.TextChoices):
    EUR = 'EUR',
    UAH = 'UAH',
    USD = 'USD'


class CurrencyTypeISOChoices(models.TextChoices):
    EUR = 978,
    UAH = 980,
    USD = 840

