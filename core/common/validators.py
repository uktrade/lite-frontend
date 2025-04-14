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


class PastDateValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if value > date.today():
            raise ValidationError(self.message)


class RelativeDeltaDateValidator:
    def __init__(self, message, **kwargs):
        self.message = message
        self.relativedelta = relativedelta(**kwargs)

    def __call__(self, value):
        if value > (date.today() + self.relativedelta):
            raise ValidationError(self.message)
