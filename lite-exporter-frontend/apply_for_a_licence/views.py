from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from applications.services import post_application
from apply_for_a_licence.initial import initial_questions


class InitialQuestions(TemplateView):
    forms = initial_questions()

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_application)

        # If there are more forms to go through, continue
        if response:
            return response

        # If there is no response (no forms left to go through), go to the overview page
        return redirect(reverse_lazy('applications:edit', kwargs={'pk': data['application']['id']}))


def check_all_parties_have_a_document(parties):
    for party in parties:
        if not party['document']:
            return False
    return True
