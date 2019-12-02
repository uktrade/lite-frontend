from django.template import Context, TemplateSyntaxError, Engine

from letter_templates.context_variables import get_context_variables
from picklists.exceptions import InvalidVarException


def template_engine_factory():
    # Put the variable name in if missing variables. Else trigger an InvalidVarException.
    string_if_invalid = InvalidVarException()
    return Engine(string_if_invalid=string_if_invalid)


def picklist_paragraph_errors(request):
    template_engine = template_engine_factory()
    try:
        template = template_engine.from_string(request.POST["text"])
        context = Context(get_context_variables())
        template.render(context)
        # Template is valid! :)
    except (TemplateSyntaxError, InvalidVarException) as err:
        # Template is invalid! :(
        return {"text": err.args}
    return None
