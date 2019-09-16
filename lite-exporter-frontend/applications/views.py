from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.components import HiddenField
from lite_forms.generators import error_page, form_page

from applications.forms import respond_to_query_form, ecju_query_respond_confirmation_form
from applications.services import get_applications, get_application, get_case_notes, \
    get_application_ecju_queries, get_ecju_query, put_ecju_query, post_application_case_notes
from core.helpers import group_notifications
from core.services import get_notifications


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        applications = get_applications(request)
        notifications = get_notifications(request, unviewed=True)

        context = {
            'title': 'Applications',
            'applications': applications,
            'notifications': group_notifications(notifications),
        }
        return render(request, 'applications/index.html', context)


class ApplicationDetailEmpty(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        return redirect(reverse_lazy('applications:application-detail', kwargs={'pk': application_id,
                                                                                'type': 'case-notes'}))


class ApplicationDetail(TemplateView):
    application_id = None
    application = None
    case_id = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs['pk'])
        application, status_code = get_application(request, self.application_id)
        self.application = application['application']
        self.case_id = self.application['case']
        self.view_type = kwargs['type']

        if self.view_type != 'case-notes' and self.view_type != 'ecju-queries':
            return Http404

        return super(ApplicationDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        # add application number to next query
        notifications = get_notifications(request, unviewed=True)
        case_note_notifications = len([x for x in notifications if x['parent'] == self.application_id
                                       and x['object'] == 'case_note'])
        ecju_query_notifications = len([x for x in notifications if x['parent'] == self.application_id
                                        and x['object_type'] == 'ecju_query'])

        context = {
            'application': self.application,
            'title': self.application['name'],
            'type': self.view_type,
            'case_note_notifications': case_note_notifications,
            'ecju_query_notifications': ecju_query_notifications,
        }

        if self.view_type == 'case-notes':
            context['notes'] = get_case_notes(request, self.case_id)['case_notes']

        if self.view_type == 'ecju-queries':
            context['open_queries'], context['closed_queries'] = get_application_ecju_queries(request, self.case_id)

        return render(request, 'applications/application.html', context)

    def post(self, request, **kwargs):
        if self.view_type != 'case-notes':
            return Http404

        response, status_code = post_application_case_notes(request, self.case_id, request.POST)

        if 'errors' in response:
            errors = response.get('errors')
            if errors.get('text'):
                error = errors.get('text')[0]
                error = error.replace('This field', 'Case note')
                error = error.replace('this field', 'the case note')  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append('{field}: {error}'.format(field=key, error=errors[key][0]))
                error = '\n'.join(error_list)
            return error_page(request, error)

        return redirect(reverse_lazy('applications:application', kwargs={'pk': self.application_id}))


class RespondToQuery(TemplateView):
    def get(self, request, **kwargs):
        """
        Will get a text area form for the user to respond to the ecju_query
        """
        application_id = str(kwargs['pk'])
        ecju_query = get_ecju_query(request, str(kwargs['pk']), str(kwargs['query_pk']))

        if ecju_query['response']:
            raise Http404

        return form_page(request, respond_to_query_form(application_id, ecju_query))

    def post(self, request, **kwargs):
        """
        will determine what form the user is on:
        if the user is on the input form will then will determine if data is valid, and move user to confirmation form
        else will allow the user to confirm they wish to respond and post data if accepted.
        """
        form_name = request.POST.get('form_name')
        application_id = str(kwargs['pk'])
        ecju_query_id = str(kwargs['query_pk'])

        ecju_query = get_ecju_query(request, application_id, ecju_query_id)

        if form_name == 'respond_to_query':
            # Post the form data to API for validation only
            data = {'response': request.POST.get('response'), 'validate_only': True}
            response, status_code = put_ecju_query(request, application_id, ecju_query_id, data)

            if status_code != 200:
                errors = response.get('errors')
                errors = {error: message for error, message in errors.items()}
                form = respond_to_query_form(application_id, ecju_query)
                data = {'response': request.POST.get('response')}
                return form_page(request, form, data=data, errors=errors)
            else:
                form = ecju_query_respond_confirmation_form(reverse_lazy('applications:respond_to_query',
                                                                         kwargs={'pk': application_id,
                                                                                 'query_pk': ecju_query_id}))
                form.questions.append(HiddenField('response', request.POST.get('response')))
                return form_page(request, form)
        elif form_name == 'ecju_query_response_confirmation':
            if request.POST.get('confirm_response') == 'yes':
                data, status_code = put_ecju_query(request, application_id, ecju_query_id,
                                                   request.POST)

                if 'errors' in data:
                    return form_page(request, respond_to_query_form(application_id, ecju_query), data=request.POST,
                                     errors=data['errors'])

                return redirect(reverse_lazy('applications:application-detail', kwargs={'pk': application_id,
                                                                                        'type': 'ecju-queries'}))
            elif request.POST.get('confirm_response') == 'no':
                return form_page(request, respond_to_query_form(application_id, ecju_query), data=request.POST)
            else:
                error = {'required': ['This field is required']}
                form = ecju_query_respond_confirmation_form(reverse_lazy('applications:respond_to_query',
                                                                         kwargs={'pk': application_id,
                                                                                 'query_pk': ecju_query_id}))
                form.questions.append(HiddenField('response', request.POST.get('response')))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(None, 'We had an issue creating your response. Try again later.')
