from django.views.generic import TemplateView
from caseworker.cases.services import get_case


class advicePlaceholderView(TemplateView):
    """This is POC ATM and should be removed with the first PR
    of advice. Currently, this is a TemplateView but it should
    be fairly simple to make this e.g. a SingleFormView.
    """

    template_name = "advice/placeholder.html"

    def get_context_data(self, **kwargs):
        case_id = str(kwargs["pk"])
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.
        case = get_case(self.request, case_id)
        return {"case": case, "greetings": "Hello advice!"}
