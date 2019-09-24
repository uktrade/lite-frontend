from django.shortcuts import render
from django.views.generic import TemplateView
from lite_forms.components import HiddenField
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from end_users.forms import apply_for_an_end_user_advisory_form, copy_end_user_advisory_form, \
    end_user_advisory_success_page
from end_users.services import get_end_user_advisories, post_end_user_advisories, get_end_user_advisory


class EndUsersList(TemplateView):
    def get(self, request, **kwargs):
        end_users = get_end_user_advisories(request)

        context = {
            'title': 'End User Advisories',
            'end_users': end_users,
        }
        return render(request, 'end_users/index.html', context)


class CopyAdvisory(TemplateView):

    forms = None
    data = None

    def dispatch(self, request, *args, **kwargs):
        query = get_end_user_advisory(request, str(kwargs['pk']))

        self.data = {
            'end_user.name': query['end_user']['name'],
            'end_user.website': query['end_user']['website'],
            'end_user.address': query['end_user']['address'],
            'end_user.country': query['end_user']['country']['id'],
            'reasoning': query.get('reasoning', ''),
            'note': query.get('note', ''),
            'copy_of': query['id'],
            'contact_email': query['contact_email'],
            'contact_telephone': query['contact_telephone']
        }

        individual, commercial = False, False

        sub_type = query['end_user']['sub_type']['key']
        if sub_type != 'individual':
            self.data['contact_name'] = query['contact_name']
            self.data['contact_job_title'] = query['contact_job_title']
        else:
            individual = True

        if sub_type == 'commercial':
            commercial = True
            self.data['nature_of_business'] = query['nature_of_business']

        self.forms = copy_end_user_advisory_form(individual, commercial)

        # Add the existing end user type as a hidden field to preserve its data
        self.forms.forms[0].questions.append(HiddenField('end_user.sub_type', query['end_user']['sub_type']['key']))

        return super(CopyAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0], data=self.data)

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories, inject_data=self.data)

        if response:
            return response

        return end_user_advisory_success_page(request, str(data['end_user_advisory']['id']))


class ApplyForAnAdvisory(TemplateView):

    forms = None

    def dispatch(self, request, *args, **kwargs):
        individual = request.POST.get('end_user.sub_type') == 'individual'
        commercial = request.POST.get('end_user.sub_type') == 'commercial'
        self.forms = apply_for_an_end_user_advisory_form(individual, commercial)

        return super(ApplyForAnAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories)

        if response:
            return response

        return end_user_advisory_success_page(request, str(data['end_user_advisory']['id']))
