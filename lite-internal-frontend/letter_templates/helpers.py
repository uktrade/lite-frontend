import os

from django.template import Engine, Context
from markdown import Markdown

from conf import settings
from letter_templates.services import get_letter_layout


class InvalidVarException(Exception):
    """
    InvalidVarException is triggered by the django template engine when it cannot
    find a context variable. This exception should be handled in places where the
    template may use an invalid variable (user entered variables)
    """

    def __mod__(self, missing):
        raise InvalidVarException("Invalid template variable {{ %s }}" % missing)

    def __contains__(self, search):
        if search == "%s":
            return True
        return False


def template_engine_factory(allow_missing_variables=False):
    """
    Create a template engine configured for use with letter templates.
    """
    # Put the variable name in if missing variables. Else trigger an InvalidVarException.
    string_if_invalid = "{{ %s }}" if allow_missing_variables else InvalidVarException()
    return Engine(
        string_if_invalid=string_if_invalid,
        dirs=[os.path.join(settings.LETTER_TEMPLATES_DIRECTORY)],
        libraries={"sass_tags": "sass_processor.templatetags.sass_tags"},
    )


def markdown_to_html(text):
    return Markdown().convert(text)


def generate_preview(layout, letter_paragraphs: list):
    django_engine = template_engine_factory(allow_missing_variables=True)

    template = django_engine.get_template(f"{layout}.html")

    letter_context = Context(
        {"content": "\n\n".join([markdown_to_html(paragraph["text"]) for paragraph in letter_paragraphs])}
    )
    return template.render(letter_context)


def get_template_content(request):
    data = request.POST.copy()

    layout = None
    if data.get("layout"):
        layout, status = get_letter_layout(request, data["layout"])
        if status != 200:
            raise RuntimeError(f"Letter layout endpoint returned { status }.")

    return {
        "name": data.get("name"),
        "layout": layout,
        "restricted_to": data.getlist("restricted_to"),
        "action": data.get("action"),
        "letter_paragraphs": data.getlist("letter_paragraphs"),
    }
