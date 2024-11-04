from core.enums.regex_enum import RegEx
from core.models import BaseModel

from django.core import validators as V
from django.db import models


class AutoParkModel(BaseModel):
    class Meta:
        db_table = 'auto_parks'
        ordering =['id']

    # name = models.CharField(max_length=20, validators=[V.RegexValidator(RegEx.AUTO_PARK_NAME.pattern, RegEx.AUTO_PARK_NAME.msg)])
    name = models.CharField(max_length=20, validators=[V.RegexValidator(*RegEx.AUTO_PARK_NAME.value)])
