import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('settings')
app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {

    'refresh_price': {
        "task": "core.services.currency_exchange_service.update_exchange_rates",
        "schedule": crontab(minute="*/2")
    },
    'refresh_iso_price': {
        "task": "core.services.currency_exchange_service.update_exchange_rates_mono",
        "schedule": crontab(minute="*/2")
    },
    'refresh_car_price': {
        "task": "core.services.currency_exchange_service.update_car_prices",
        "schedule": crontab(minute="*/2")
    }
}
