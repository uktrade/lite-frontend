from django.forms import widgets


class Autocomplete(widgets.Select):
    template_name = "forms/autocomplete_field.html"
