from rest_framework import serializers

from apps.price_convertor.models import ExchangeRateISOModel, ExchangeRateModel


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateModel
        fields = '__all__'


class ExchangeRateISOSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateISOModel
        fields = '__all__'
