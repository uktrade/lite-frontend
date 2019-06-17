import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cases.forms.denial_reasons import denial_reasons_form
from cases.services import get_case, get_case_notes, post_case_notes, put_applications
from conf import client
from conf.settings import env
from libraries.forms.generators import error_page, form_page
from libraries.forms.submitters import submit_single_form


def index(request):
    queue_id = request.GET.get('queue')

    # If a queue id is not provided, use the default queue
    if not queue_id:
        queue_id = '00000000-0000-0000-0000-000000000001'

    queues = client.get(request, '/queues/').json()
    response = client.get(request, '/queues/' + queue_id).json()

    context = {
        'queues': queues,
        'queue_id': queue_id,
        'data': response,
        'title': response.get('queue').get('name'),
    }
    return render(request, 'cases/index.html', context)


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        case_notes, status_code = get_case_notes(request, case_id)

        context = {
            'data': case,
            'title': case.get('case').get('application').get('name'),
            'case_notes': case_notes.get('case_notes'),
        }
        return render(request, 'cases/case/index.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:
            error = response.get('errors').get('text')[0]
            error = error.replace('This field', 'Case note')
            error = error.replace('this field', 'the case note')
            return error_page(request, error)

        return redirect('/cases/' + case_id + '#case_notes')


class ManageCase(TemplateView):

    def get(self, request, pk):
        response = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/').json()
        context = {
          'data': response,
          'title': 'Manage ' + response.get('case').get('application').get('name'),
        }
        return render(request, 'cases/manage.html', context)

    def post(self, request, pk):
        applicant_case = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/').json()
        case_id = applicant_case.get('case').get('id')
        application_id = applicant_case.get('case').get('application').get('id')

        # PUT form data
        response = requests.put(env("LITE_API_URL") + '/applications/' + application_id + '/',
                                json=request.POST).json()

        if 'errors' in response:
            return redirect('/cases/' + case_id + '/manage')

        return redirect('/cases/' + case_id)


class DecideCase(TemplateView):
    def get(self, request, pk):
        response = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/').json()
        context = {
          'data': response,
          'title': 'Manage ' + response.get('case').get('application').get('name'),
        }
        return render(request, 'cases/decide.html', context)

    def post(self, request, pk):
        applicant_case = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/').json()
        case_id = applicant_case.get('case').get('id')
        application_id = applicant_case.get('case').get('application').get('id')

        if request.POST['status'] == 'declined':
            return redirect(reverse('cases:deny', kwargs={'pk': str(pk)}))

        # PUT form data
        response = requests.put(env("LITE_API_URL") + '/applications/' + application_id + '/',
                                json=request.POST).json()

        if 'errors' in response:
            return redirect('/cases/' + case_id + '/manage')

        return redirect('/cases/' + case_id)


class DenyCase(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, denial_reasons_form())

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        application_id = case['case']['application']['id']

        data = {
            'reasons': request.POST.getlist('reasons'),
            'reason_details': request.POST['reason_details'],
            'status': 'under_final_review',
        }

        response, data = submit_single_form(request,
                                            denial_reasons_form(),
                                            put_applications,
                                            pk=application_id,
                                            override_data=data)

        if response:
            return response

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse('cases:case', kwargs={'pk': case_id}))

