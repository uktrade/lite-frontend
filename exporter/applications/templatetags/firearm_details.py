from django import template

from exporter.goods.forms.firearms import FirearmFirearmAct1968Form


register = template.Library()


@register.filter(name="firearm_act_section_label")
def firearm_act_section_label(value):
    return FirearmFirearmAct1968Form.SectionChoices(value).label
