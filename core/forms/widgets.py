from django.forms import widgets


class Autocomplete(widgets.Select):
    template_name = "forms/autocomplete_field.html"


class GridmultipleSelect(widgets.ChoiceWidget):
    allow_multiple_selected = True
    input_type = "checkbox"
    template_name = "forms/checkbox_select.html"
    option_template_name = "forms/checkbox_option.html"
