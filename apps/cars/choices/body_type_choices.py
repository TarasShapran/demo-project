from django.db import models


class BodyTypeChoices(models.TextChoices):
    Hatchback = 'Hatchback',
    Sedan = 'Sedan',
    Coupe = 'Coupe',
    Jeep = 'Jeep'
