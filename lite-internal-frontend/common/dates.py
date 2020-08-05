from django.utils import timezone


def api_date(day, month, year):
    """
    Convert day month and year parameters into expected API str format.

    Format: %Y-%m-%d
    """
    date = timezone.datetime(year=int(year), month=int(month), day=int(day))
    return date.strftime("%Y-%m-%d")
