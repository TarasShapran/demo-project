import logging
from decimal import Decimal
from typing import List

from core.enums.currency_code import CurrencyCodeEnum

from rest_framework import serializers

from apps.cars.choices.body_type_choices import CurrencyTypeChoices
from apps.cars.models import CarCurrencyPriceModel, CarImagesModel, CarModel
from apps.price_convertor.models import ExchangeRateISOModel, ExchangeRateModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImagesModel
        fields = ('image',)


class CarCurrencyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCurrencyPriceModel
        fields = ('currency', 'amount',)


class CarSerializer(serializers.ModelSerializer):
    car_images = CarPhotoSerializer(read_only=True, many=True)
    car_currency_prices = CarCurrencyPriceSerializer(read_only=True, many=True)

    class Meta:
        model = CarModel
        fields = (
            'id', 'brand', 'price', 'currency', 'year', 'body', 'region', 'car_currency_prices', 'car_images',
            'created_at',
            'updated_at')

    def save(self, **kwargs):
        super().save(**kwargs)
        if (base_price := self.instance.price) and (base_currency := self.instance.currency):
            currency_rates_map = dict()
            currency_rates: List[ExchangeRateISOModel] = ExchangeRateISOModel.objects.all()
            for currency_rate in currency_rates:
                currency_rates_map[(currency_rate.currencyCodeA, currency_rate.currencyCodeB)] = currency_rate.rateSell
                currency_rates_map[(currency_rate.currencyCodeB, currency_rate.currencyCodeA)] = currency_rate.rateBuy

            for currency_code in CurrencyCodeEnum:
                iso_currency, currency = currency_code.code, currency_code.currency
                exchange_rate = currency_rates_map.get(
                    (int(iso_currency), CurrencyCodeEnum[base_currency].code))
                converted_amount = None
                if currency.upper() == base_currency:
                    converted_amount = base_price
                    exchange_rate = True

                if not exchange_rate:
                    continue
                if currency.upper() != base_currency and base_currency == CurrencyCodeEnum.EUR.currency:
                    converted_amount = base_price * Decimal(exchange_rate)
                elif currency.upper() != base_currency and base_currency == CurrencyCodeEnum.UAH.currency:
                    converted_amount = base_price / Decimal(exchange_rate)
                elif currency.upper() != base_currency and base_currency == CurrencyCodeEnum.USD.currency:
                    if currency.upper() == CurrencyCodeEnum.UAH.currency:
                        converted_amount = base_price * Decimal(exchange_rate)
                    else:
                        converted_amount = base_price / Decimal(exchange_rate)

                if not converted_amount:
                    continue
                data = {
                    'currency': currency.upper(),
                    'amount': round(converted_amount, 2)
                }
                car_currency_serializer = CarCurrencyPriceSerializer(data=data)
                car_currency_serializer.is_valid(raise_exception=True)
                car_currency_serializer.save(car=self.instance)

        return CarModel.objects.all().filter(id=self.instance.id)

    # def validate_brand(self, brand):
    #     if brand == 'Sas':
    #         raise serializers.ValidationError({'detail': 'brand == Sas'})
    #     return brand
    #
    # def validate(self, attrs):
    #     price_convertor = attrs['price_convertor']
    #     year = attrs['year']
    #     if price_convertor == year:
    #         raise serializers.ValidationError({'detail': 'year==price_convertor'})
    #     return attrs
