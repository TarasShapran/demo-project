from rest_framework import serializers

from apps.cars.choices.body_type_choices import CurrencyTypeChoices
from apps.cars.models import CarCurrencyPriceModel, CarImagesModel, CarModel
from apps.price_convertor.models import ExchangeRateModel


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
        fields = ('id', 'brand', 'price', 'currency', 'year', 'body', 'car_currency_prices', 'car_images', 'created_at',
                  'updated_at')

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.instance.price and self.instance.currency:
            exchange_rate = ExchangeRateModel.objects.all()
            for item, _ in CurrencyTypeChoices.choices:
                if item != self.instance.currency:
                    car_currency_data = {'currency': item, 'amount': round(self.instance.price / 38, 2)}
                    car_currency_serializer = CarCurrencyPriceSerializer(data=car_currency_data)
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
