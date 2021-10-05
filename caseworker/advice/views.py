from django.views.generic import TemplateView
from caseworker.cases.services import get_case


class CaseContextMixin:
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """
    def get_context(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(CaseContextMixin, self).get_context_data(**kwargs)
        case_id = str(kwargs["pk"])
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.
        case = get_case(self.request, case_id)
        return {**context, **self.get_context(), "case": case}


class AdvicePlaceholderView(CaseContextMixin, TemplateView):
    """This is POC ATM and should be removed with the first PR
    of advice. Currently, this is a TemplateView but it should
    be fairly simple to make this e.g. a SingleFormView.
    """

    template_name = "advice/placeholder.html"

    def get_context(self):
        return {"greetings": "Hello World!"}


