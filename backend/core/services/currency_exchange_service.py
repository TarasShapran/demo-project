import logging

import requests
from configs.celery import app

from apps.price_convertor.models import ExchangeRateModel
from apps.price_convertor.serializers import ExchangeRateSerializer

logger = logging.getLogger(__name__)


class ExchangeRateService:
    PRIVATBANK_API_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

    @staticmethod
    @app.task
    def __get_exchange_rates_from_privatbank():
        response = requests.get(ExchangeRateService.PRIVATBANK_API_URL)
        if response.status_code == 200:
            return response.json()
        return []

    @staticmethod
    @app.task
    def update_exchange_rates():
        exchange_rates = ExchangeRateService.__get_exchange_rates_from_privatbank()

        for rate_data in exchange_rates:
            ccy = rate_data['ccy']
            base_ccy = rate_data['base_ccy']
            existing_rate = ExchangeRateModel.objects.filter(ccy=ccy, base_ccy=base_ccy).first()

            if existing_rate:
                serializer = ExchangeRateSerializer(existing_rate, data=rate_data)
            else:
                serializer = ExchangeRateSerializer(data=rate_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
