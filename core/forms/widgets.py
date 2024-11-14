from django.forms import widgets


class Autocomplete(widgets.Select):
    template_name = "forms/autocomplete_field.html"


class GridmultipleSelect(widgets.ChoiceWidget):
    allow_multiple_selected = True
    input_type = "checkbox"
    template_name = "forms/checkbox_select.html"
    option_template_name = "forms/checkbox_option.html"


class CheckboxInputSmall(widgets.ChoiceWidget):
    input_type = "checkbox"
    template_name = "forms/checkbox_select.html"
    option_template_name = "forms/checkbox_option.html"


class FilterSelect(widgets.Select):
    template_name = "forms/filter_select.html"

    def __init__(self, parent_select_name, attrs=None, choices=()):
        super().__init__(attrs, choices)
        self.parent_select_name = parent_select_name

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        # This enriches the select with any attrs that are set during creation
        # data-attribute is used for filtering the options availble in JS
        option = super().create_option(name, value, label, selected, index, subindex=None, attrs=None)
        if hasattr(self.choices[int(option["index"])], "attrs"):
            option["attrs"].update(self.choices[int(option["index"])].attrs)
        return option

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["parent_select_name"] = self.parent_select_name
        return context
