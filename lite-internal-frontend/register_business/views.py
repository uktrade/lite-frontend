from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from organisations.services import post_organisations
from register_business.forms import register_business_forms


class RegisterBusiness(TemplateView):
    forms = None

    def dispatch(self, request, *args, **kwargs):
        individual = request.POST.get('sub_type') == 'individual'
        self.forms = register_business_forms(individual)

        return super(RegisterBusiness, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, self.forms, post_organisations)

        if response:
            return response

        messages.success(request, 'The organisation was created successfully')
        return redirect('organisations:organisations')
