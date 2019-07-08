from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cases.forms.denial_reasons import denial_reasons_form
from cases.forms.move_case import move_case_form
from cases.forms.record_decision import record_decision_form
from cases.services import get_case, post_case_notes, put_applications, get_activity, put_case
from conf.constants import DEFAULT_QUEUE_ID
from core.services import get_queue, get_queues
from libraries.forms.generators import error_page, form_page
from libraries.forms.submitters import submit_single_form
from queues.helpers import add_assigned_users_to_cases
from queues.services import get_queue_case_assignments


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to that queue
        """
        queue_id = request.GET.get('queue', DEFAULT_QUEUE_ID)
        queues, status_code = get_queues(request)
        queue, status_code = get_queue(request, queue_id)
        case_assignments, status_code = get_queue_case_assignments(request, queue_id)

        # Add assigned users to each case
        queue['queue']['cases'] = add_assigned_users_to_cases(queue['queue']['cases'],
                                                              case_assignments['case_assignments'])

        context = {
            'queues': queues,
            'queue_id': queue_id,
            'data': queue,
            'title': queue.get('queue').get('name'),
        }
        return render(request, 'cases/index.html', context)

    def post(self, request, **kwargs):
        """
        Assign users depending on what cases were selected
        """
        queue_id = request.GET.get('queue', DEFAULT_QUEUE_ID)
        return redirect(reverse('queues:case_assignments', kwargs={'pk': queue_id}) + '?cases=' + ','.join(request.POST.getlist('cases')))


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        activity, status_code = get_activity(request, case_id)

        context = {
            'data': case,
            'title': case.get('case').get('application').get('name'),
            'activity': activity.get('activity'),
        }
        return render(request, 'cases/case/index.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:
            error = response.get('errors').get('text')[0]
            error = error.replace('This field', 'Case note')
            error = error.replace('this field', 'the case note')  # TODO: Move to API
            return error_page(request, error)

        return redirect('/cases/' + case_id + '#case_notes')


class ManageCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        context = {
            'data': case,
            'title': 'Manage ' + case.get('case').get('application').get('name'),
        }
        return render(request, 'cases/manage.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        application_id = case.get('case').get('application').get('id')

        # PUT form data
        data, status_code = put_applications(request, application_id, request.POST)

        if 'errors' in data:
            return redirect('/cases/' + case_id + '/manage')

        return redirect('/cases/' + case_id)


class DecideCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        if case['case']['application']['status'] == 'approved':
            data = {
                'status': case['case']['application']['status']
            }
        elif case['case']['application']['status'] == 'under_final_review':
            data = {
                'status': 'declined'
            }
        else:
            data = {}

        return form_page(request, record_decision_form(), data=data)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        case_id = case.get('case').get('id')
        application_id = case.get('case').get('application').get('id')

        if not request.POST.get('status'):
            return form_page(request, record_decision_form(), errors={
                'status': ['Select an option']
            })

        if request.POST.get('status') == 'declined':
            return redirect(reverse('cases:deny', kwargs={'pk': case_id}))

        # PUT form data
        put_applications(request, application_id, request.POST)

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


class MoveCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        return form_page(request,
                         move_case_form(request, reverse('cases:case', kwargs={'pk': case_id})),
                         data=case['case'])

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])

        data = {
            'queues': request.POST.getlist('queues'),
        }

        response, data = submit_single_form(request,
                                            move_case_form(request, reverse('cases:case', kwargs={'pk': case_id})),
                                            put_case,
                                            pk=case_id,
                                            override_data=data)

        if response:
            return response

        return redirect(reverse('cases:case', kwargs={'pk': case_id}))
