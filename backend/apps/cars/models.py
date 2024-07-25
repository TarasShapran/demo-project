import os
from datetime import datetime

from core.enums.regex_enum import RegEx
from core.models import BaseModel
from core.services.photo_service import PhotoService
from core.services.s3_service import AVATAR_LOCATION, CarStorage
from pytz import utc

from django.contrib.auth import get_user_model
from django.core import validators as V
from django.db import models

from apps.auto_parks.models import AutoParkModel
from apps.cars.choices.body_type_choices import BodyTypeChoices, CurrencyTypeChoices, Region_Choiceas
from apps.cars.managers import CarManager
from apps.price_convertor.models import ExchangeRateModel
from apps.users.models import UserModel

# UserModel = get_user_model()


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ['-id']

    brand = models.CharField(max_length=20, validators=[V.RegexValidator(RegEx.BRAND.pattern, RegEx.BRAND.msg)])
    # price_convertor = models.IntegerField(validators=[V.MinValueValidator(0), V.MaxValueValidator(10000000)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=9, choices=CurrencyTypeChoices.choices)
    year = models.IntegerField(validators=[V.MinValueValidator(1800), V.MaxValueValidator(datetime.now().year)])
    body = models.CharField(max_length=9, choices=BodyTypeChoices.choices)
    auto_park = models.ForeignKey(AutoParkModel, on_delete=models.CASCADE, related_name='cars')
    region = models.CharField(max_length=20, choices=Region_Choiceas.choices)
    # def save(self, *args, **kwargs):
    #     if self.price and self.currency:
    #         exchange_rate = ExchangeRateModel.objects.all()
    #         for item, _ in CurrencyTypeChoices.choices:
    #             if item != self.currency:
    #
    #                 car_currency = CarCurrencyPriceModel()
    #                 car_currency.save()

    objects = models.Manager()
    my_objects = CarManager()


class CarDetailsModel(BaseModel):
    class Meta:
        db_table = 'car_details'

    views = models.IntegerField(default=0)
    user_viewed = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='viewed_cars')
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_details')


class CarImagesModel(BaseModel):
    class Meta:
        db_table = 'car_images'

    image = models.ImageField(storage=CarStorage())
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_images')

    def save(self, *args, **kwargs):
        if self.image:
            brand = self.car.brand
            self.image.storage.location = f"{AVATAR_LOCATION}/{brand}/{self.car_id}"
        super(CarImagesModel, self).save(*args, **kwargs)


class CarCurrencyPriceModel(BaseModel):
    class Meta:
        db_table = 'car_currency_price'

    currency = models.CharField(max_length=3, choices=CurrencyTypeChoices.choices)  # USD, EUR, UAH
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_currency_prices')
