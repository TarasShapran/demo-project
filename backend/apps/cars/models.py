import os
from datetime import datetime

from core.enums.regex_enum import RegEx
from core.models import BaseModel
from core.services.photo_service import PhotoService
from core.services.s3_service import AVATAR_LOCATION, CarStorage
from pytz import utc

from django.core import validators as V
from django.db import models

from apps.auto_parks.models import AutoParkModel
from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.managers import CarManager


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ['-id']

    brand = models.CharField(max_length=20, validators=[V.RegexValidator(RegEx.BRAND.pattern, RegEx.BRAND.msg)])
    price = models.IntegerField(validators=[V.MinValueValidator(0), V.MaxValueValidator(10000000)])
    year = models.IntegerField(validators=[V.MinValueValidator(1800), V.MaxValueValidator(datetime.now().year)])
    body = models.CharField(max_length=9, choices=BodyTypeChoices.choices)
    auto_park = models.ForeignKey(AutoParkModel, on_delete=models.CASCADE, related_name='cars')

    objects = models.Manager()
    my_objects = CarManager()


class CarImagesModel(BaseModel):
    class Meta:
        db_table = 'car_images'

    image = models.ImageField(storage=CarStorage())
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_images')

    def save(self, *args, **kwargs):
        if self.image:
            brand = self.car.brand
            file_ext = os.path.splitext(str(self.image.name))[-1]
            self.image.name = f"car_image{file_ext}"
            self.image.storage.location = f"{AVATAR_LOCATION}/{brand}/{self.car_id}"
        super(CarImagesModel, self).save(*args, **kwargs)
