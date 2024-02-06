from rest_framework import serializers

from apps.price_convertor.models import ExchangeRateModel


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateModel
        fields = '__all__'
