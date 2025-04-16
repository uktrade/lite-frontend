from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError


class FutureDateValidator:
    def __init__(self, message, include_today=False):
        self.message = message
        self.include_today = include_today

    def __call__(self, value):
        if value == date.today() and self.include_today:
            return
        if value <= date.today():
            raise ValidationError(self.message)
