import os

import requests
from configs.celery import app
from core.dataclasses.user_dataclass import UserDataClass
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from apps.price_convertor.models import ExchangeRateModel
from apps.price_convertor.serializers import ExchangeRateSerializer

UserModel = get_user_model()


class EmailService:
    @staticmethod
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def register_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email.delay(
            user.email,
            'register.html',
            {'name': user.profile.name, 'url': url},
            'Register'
        )

    @classmethod
    def recovery_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email(user.email, 'recovery.html', {'url': url}, 'Recovery password')

    @staticmethod
    @app.task
    def spam():
        for user in UserModel.objects.all():
            EmailService.__send_email(user.email, 'spam.html', {}, 'SPAM')


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     PRIVATBANK_API_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
#
#     @staticmethod
#     @app.task
#     def __get_exchange_rates_from_privatbank():
#         response = requests.get(EmailService.PRIVATBANK_API_URL)
#         if response.status_code == 200:
#             return response.json()
#         return []
#
#     @staticmethod
#     @app.task
#     def update_exchange_rates():
#         exchange_rates = EmailService.__get_exchange_rates_from_privatbank()
#
#         for rate_data in exchange_rates:
#             ccy = rate_data['ccy']
#             base_ccy = rate_data['base_ccy']
#             existing_rate = ExchangeRateModel.objects.filter(ccy=ccy, base_ccy=base_ccy).first()
#
#             if existing_rate:
#                 serializer = ExchangeRateSerializer(existing_rate, data=rate_data)
#             else:
#                 serializer = ExchangeRateSerializer(data=rate_data)
#
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
