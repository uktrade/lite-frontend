from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from applications.forms.told_by_an_official import told_by_an_official_form
from applications.services import get_application, put_application


class ApplicationEditToldByAnOfficial(TemplateView):
    application_id = None
    application = None
    form = told_by_an_official_form()

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs['pk'])
        self.application = get_application(request, self.application_id)

        return super(ApplicationEditToldByAnOfficial, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=self.application)

    def post(self, request, **kwargs):
        response, _ = submit_single_form(request, self.form, put_application, pk=self.application_id)

        # If there are more forms to go through, continue
        if response:
            return response

        return redirect(reverse_lazy('applications:edit', kwargs={'pk': self.application_id}))
