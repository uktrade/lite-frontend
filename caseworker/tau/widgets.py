from django.forms import widgets


class GoodsMultipleSelect(widgets.ChoiceWidget):
    allow_multiple_selected = True
    input_type = "checkbox"
    template_name = "tau/goods_checkbox_select.html"
    option_template_name = "tau/goods_checkbox_option.html"
