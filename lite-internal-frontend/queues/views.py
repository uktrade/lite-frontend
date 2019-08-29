from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from lite_forms.generators import form_page, error_page

from cases.forms.assign_users import assign_users_form
from queues import forms
from queues.helpers import get_assigned_users_from_cases
from queues.services import get_queue, get_queues, \
    post_queues, put_queue, put_queue_case_assignments, get_queue_case_assignments
from users.services import get_gov_user


class QueuesList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_queues(request)
        user_data, status_code = get_gov_user(request, str(request.user.lite_api_user_id))

        context = {
            'data': data,
            'title': 'Queues',
            'user_data': user_data,
        }
        return render(request, 'queues/index.html', context)


class AddQueue(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add Queue',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        # including the user's team details in the post request
        user_data, status_code = get_gov_user(request, str(request.user.lite_api_user_id))
        post_data = request.POST.copy()
        post_data['team'] = user_data['user']['team']['id']
        data, status_code = post_queues(request, post_data)

        if status_code == 400:
            context = {
                'title': 'Add Queue',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('queues:queues'))


class EditQueue(TemplateView):
    def get(self, request, **kwargs):
        queue_id = str(kwargs['pk'])
        data, status_code = get_queue(request, queue_id)
        context = {
            'data': data.get('queue'),
            'title': 'Edit Queue',
            'page': forms.edit_form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = put_queue(request, str(kwargs['pk']), request.POST)
        if status_code == 400:
            context = {
                'title': 'Add Queue',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('queues:queues'))


class CaseAssignments(TemplateView):
    def get(self, request, **kwargs):
        """
        Assign users to cases
        """

        queue_id = str(kwargs['pk'])
        queue, status_code = get_queue(request, queue_id)
        case_assignments, status_code = get_queue_case_assignments(request, queue_id)

        case_ids = request.GET.get('cases').split(',')
        user_data, status_code = get_gov_user(request, str(request.user.lite_api_user_id))

        # If no cases have been selected, return an error page
        if not request.GET.get('cases'):
            return error_page(request, 'Invalid case selection')

        # Get assigned users
        assigned_users = get_assigned_users_from_cases(case_ids, case_assignments['case_assignments'])

        return form_page(request,
                         assign_users_form(request,
                                           user_data['user']['team']['id'],
                                           queue['queue'],
                                           len(case_ids) > 1),
                         data={'users': assigned_users})

    def post(self, request, **kwargs):
        """
        Update the queue's case assignments
        """

        queue_id = str(kwargs['pk'])
        queue, status_code = get_queue(request, queue_id)
        case_ids = request.GET.get('cases').split(',')
        user_data, status_code = get_gov_user(request, str(request.user.lite_api_user_id))

        data = {
            'case_assignments': []
        }

        # Append case and users to case assignments
        for case_id in case_ids:
            data['case_assignments'].append(
                {
                    'case_id': case_id,
                    'users': request.POST.getlist('users')
                }
            )

        response, status_code = put_queue_case_assignments(request, queue_id, data)

        if 'errors' in response:
            return form_page(request, assign_users_form(request,
                                                        user_data['user']['team']['id'],
                                                        queue['queue'],
                                                        len(case_ids) > 1),
                             data=request.POST,
                             errors=response['errors'])

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse('cases:cases'))
