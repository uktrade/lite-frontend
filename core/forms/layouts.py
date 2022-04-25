from crispy_forms.layout import TemplateNameMixin
from crispy_forms.utils import render_field, TEMPLATE_PACK

from crispy_forms_gds.layout import Field, HTML

from django.template.loader import render_to_string


def summary_list(items):
    beginning = '<dl class="govuk-summary-list govuk-summary-list--no-border">'
    rows = [
        f"""
            <div class="govuk-summary-list__row">
                <dt class="govuk-summary-list__key">{key}</dt>
                <dd class="govuk-summary-list__value">{value}</dd>
            </div>
        """
        for key, value in items
    ]
    end = "</dl>"
    snippet = "".join([beginning, *rows, end])
    return HTML(snippet)


class ConditionalQuestion(TemplateNameMixin):
    template = "%s/layout/conditional_question.html"

    def __init__(self, value, *fields):
        self.value = value
        self.fields = list(fields)

    def render(self, bound_field, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)

        mapped_choices = {choice[1]: choice for choice in bound_field.field.choices}
        value = self.value
        choice = mapped_choices[value]
        position = list(mapped_choices.keys()).index(self.value)

        conditional_content = ""
        for field in self.fields:
            conditional_content += render_field(field, form, form_style, context, template_pack=template_pack, **kwargs)

        context.update(
            {"choice": choice, "field": bound_field, "position": position, "conditional_content": conditional_content}
        )

        return render_to_string(template, context.flatten())


class ConditionalRadios(TemplateNameMixin):
    template = "%s/layout/conditional_radios.html"

    def __init__(self, field, *choices):
        if not isinstance(field, str):
            raise TypeError(f"{self.__class__.__name__} only accepts field as a string parameter")

        self.field = field
        self.choices = list(choices)

    def render_choices(self, bound_field, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        to_render = []
        for value in self.choices:
            if not isinstance(value, (str, ConditionalQuestion)):
                raise TypeError("Only accepts values of type str or ConditionalQuestions")
            if isinstance(value, str):
                value = ConditionalQuestion(value)
            to_render.append(value)

        return "".join([t.render(bound_field, form, form_style, context, template_pack, **kwargs) for t in to_render])

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)

        bound_field = form[self.field]

        context.update(
            {"choices": self.render_choices(bound_field, form, form_style, context, template_pack, **kwargs)}
        )

        return render_to_string(template, context.flatten())


class ConditionalCheckbox(TemplateNameMixin):
    template = "%s/layout/conditional_checkbox.html"

    def __init__(self, field, *fields):
        if not isinstance(field, str):
            raise TypeError(f"{self.__class__.__name__} only accepts field as a string parameter")

        self.field = field
        self.fields = list(fields)

    def render_fields(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return "".join(
            [
                render_field(field, form, form_style, context, template_pack=template_pack, **kwargs)
                for field in self.fields
            ]
        )

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)

        bound_field = form[self.field]
        conditional_control = f"conditional-{bound_field.html_name}"
        bound_field.field.widget.attrs = {"data-aria-controls": conditional_control}

        conditional_content = ""
        for field in self.fields:
            conditional_content += render_field(field, form, form_style, context, template_pack=template_pack, **kwargs)

        context.update(
            {
                "field": bound_field,
                "conditional_control": conditional_control,
                "conditional_content": conditional_content,
            }
        )

        return render_to_string(template, context.flatten())


class Prefixed(Field):
    def __init__(self, prefix, field, **kwargs):
        super().__init__(field, context={"prefix": prefix}, template="%s/layout/prefixed_field.html", **kwargs)
