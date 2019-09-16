from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page, success_page
from lite_forms.submitters import submit_paged_form

from core.builtins.custom_tags import reference_code
from end_users.forms import apply_for_an_end_user_advisory_form
from end_users.services import get_end_user_advisories, post_end_user_advisories


class EndUsersList(TemplateView):
    def get(self, request, **kwargs):
        end_users = get_end_user_advisories(request)

        context = {
            'title': 'End User Advisories',
            'end_users': end_users,
        }
        return render(request, 'end_users/index.html', context)


class ApplyForAnAdvisory(TemplateView):

    forms = None

    def dispatch(self, request, *args, **kwargs):
        self.forms = apply_for_an_end_user_advisory_form()

        return super(ApplyForAnAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories)

        if response:
            return response

        return success_page(request,
                            title='Query sent successfully',
                            secondary_title='Your reference code: ' + reference_code(str(data['end_user_advisory']['id'])),
                            description='The Department for International Trade usually takes two working days to check an importer.',
                            what_happens_next=['You\'ll receive an email from DIT when your check is finished.'],
                            links={
                                'View your list of end user advisories': reverse_lazy('end_users:end_users'),
                                'Apply for another advisory': reverse_lazy('end_users:apply'),
                                'Return to Exporter Hub': reverse_lazy('core:hub'),
                            })
