from django.template import Context, TemplateSyntaxError

from letter_templates.context_variables import context_variables
from letter_templates.helpers import template_engine_factory, InvalidVarException


def picklist_paragraph_errors(request):
    template_engine = template_engine_factory(allow_missing_variables=False)
    try:
        template = template_engine.from_string(request.POST["text"])
        context = Context(context_variables)
        template.render(context)
        # Template is valid! :)
    except (TemplateSyntaxError, InvalidVarException) as err:
        # Template is invalid! :(
        return {"text": err.args}
    return None
