from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from lite_forms.components import Option, HiddenField
from lite_forms.generators import error_page, form_page
from lite_forms.submitters import submit_single_form
from s3chunkuploader.file_handler import S3FileUploadHandler, s3_client

from cases.forms.attach_documents import attach_documents_form
from cases.forms.create_ecju_query import create_ecju_query_write_or_edit_form, choose_ecju_query_type_form, \
    create_ecju_create_confirmation_form
from cases.forms.denial_reasons import denial_reasons_form
from cases.forms.move_case import move_case_form
from cases.forms.record_decision import record_decision_form
from cases.services import post_case_documents, get_case_documents, get_case_document, get_document
from cases.services import get_case, post_case_notes, put_applications, get_activity, put_case, put_clc_queries, \
    put_case_flags, get_ecju_queries, post_ecju_query

from conf import settings
from conf.constants import DEFAULT_QUEUE_ID, MAKE_FINAL_DECISIONS, OPEN_CASES_SYSTEM_QUEUE_ID, ALL_CASES_SYSTEM_QUEUE_ID
from conf.decorators import has_permission
from conf.settings import AWS_STORAGE_BUCKET_NAME
from core.builtins.custom_tags import get_string
from core.helpers import convert_dict_to_query_params
from core.services import get_user_permissions, get_statuses
from flags.services import get_flags_case_level_for_team
from picklists.services import get_picklists, get_picklist_item
from queues.helpers import add_assigned_users_to_cases
from queues.services import get_queue_case_assignments, get_queue, get_queues, get_queue_cases


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to that queue
        """
        case_type = request.GET.get('case_type')
        status = request.GET.get('status')
        statuses, status_code = get_statuses(request)
        sort = request.GET.get('sort')
        queue_id = request.GET.get('queue', DEFAULT_QUEUE_ID)
        queues, status_code = get_queues(request, include_system_queues=True)
        queue, status_code = get_queue(request, queue_id, case_type, status, sort)

        # Page parameters
        params = {'queue': queue_id, 'page': int(request.GET.get('page', 1))}
        if sort:
            params['sort'] = sort
        if status:
            params['status'] = status
        if case_type:
            params['case_type'] = case_type

        cases = get_queue_cases(request, queue_id, convert_dict_to_query_params(params))

        context = {
            'title': queue['queue'].get('name'),
            'queues': queues['queues'],
            'current_queue': queue['queue'],
            'cases': cases,
            'page': params.pop('page'),
            'statuses': statuses,
            'params': params,
            'params_str': convert_dict_to_query_params(params)
        }
        return render(request, 'cases/index.html', context)

    def post(self, request, **kwargs):
        """
        Assign users depending on what cases were selected
        """
        queue_id = request.GET.get('queue', DEFAULT_QUEUE_ID)
        return redirect(reverse('queues:case_assignments', kwargs={'pk': queue_id}) + '?cases=' + ','.join(
            request.POST.getlist('cases')))


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        queue_id = request.GET.get('return_to', DEFAULT_QUEUE_ID)
        queue, status_code = get_queue(request, queue_id)
        case, status_code = get_case(request, case_id)
        case = case['case']
        activity, status_code = get_activity(request, case_id)
        permissions = get_user_permissions(request)

        if case['type']['key'] == 'clc_query':
            context = {
                'title': 'Case',
                'case': case,
                'good': case['clc_query']['good'],
                'case_id': case_id,
                'activity': activity.get('activity'),
                'permissions': permissions,
                'queue': queue,
            }
            return render(request, 'cases/case/clc-query-case.html', context)
        else:
            context = {
                'case': case,
                'title': case.get('application').get('name'),
                'activity': activity.get('activity'),
                'permissions': permissions,
                'queue': queue,
            }
            return render(request, 'cases/case/application-case.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:

            errors = response.get('errors')
            if errors.get('text'):
                error = errors.get('text')[0]
                error = error.replace('This field', 'Case note')
                error = error.replace('this field', 'the case note')  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
                error = '\n'.join(error_list)
            return error_page(request, error)

        return redirect(reverse('cases:case', kwargs={'pk': case_id}) + '#case_notes')


class ViewAdvice(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        activity, status_code = get_activity(request, case_id)
        permissions = get_user_permissions(request)

        context = {
            'data': case,
            'title': case.get('case').get('application').get('name'),
            'activity': activity.get('activity'),
            'permissions': permissions,
            'edit_case_flags': get_string('cases.case.edit_case_flags')
        }
        return render(request, 'cases/case/advice-view.html', context)


class ViewEcjuQueries(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        ecju_queries, status_code = get_ecju_queries(request, case_id)

        context = {
            'case_id': case_id,
            'ecju_queries': ecju_queries.get('ecju_queries')
        }
        return render(request, 'cases/case/ecju-queries.html', context)


class CreateEcjuQuery(TemplateView):
    NEW_QUESTION_DDL_ID = 'new_question'

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        picklists, status = get_picklists(request, 'ecju_query', False)
        picklists = picklists.get('picklist_items')
        picklist_choices = [Option(self.NEW_QUESTION_DDL_ID, 'Write a new question')] + \
                           [Option(picklist.get('id'), picklist.get('name')) for picklist in picklists]
        form = choose_ecju_query_type_form(
            reverse('cases:ecju_queries', kwargs={'pk': case_id}),
            picklist_choices
        )

        return form_page(request, form, extra_data={'case_id': case_id})

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        form_name = request.POST.get('form_name')

        if form_name == 'ecju_query_type_select':
            return self._handle_ecju_query_type_select_post(request, case_id)

        elif form_name == 'ecju_query_write_or_edit_question':
            return self._handle_ecju_query_write_or_edit_post(case_id, request)

        elif form_name == 'ecju_query_create_confirmation':
            return self._handle_ecju_query_confirmation_post(case_id, request)

        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(None, 'We had an issue creating your question. Try again later.')

    def _handle_ecju_query_type_select_post(self, request, case_id):
        picklist_selection = request.POST.get('picklist')

        if picklist_selection != self.NEW_QUESTION_DDL_ID:
            picklist_item_text = get_picklist_item(request, picklist_selection)[0]['picklist_item']['text']
        else:
            picklist_item_text = ''

        form = create_ecju_query_write_or_edit_form(reverse('cases:ecju_queries_add', kwargs={'pk': case_id}))
        data = {'question': picklist_item_text}

        return form_page(request, form, data=data)

    def _handle_ecju_query_write_or_edit_post(self, case_id, request):
        # Post the form data to API for validation only
        data = {'question': request.POST.get('question'), 'validate_only': True}
        ecju_query, status_code = post_ecju_query(request, case_id, data)

        if status_code != 200:
            return self._handle_ecju_query_form_errors(case_id, ecju_query, request)
        else:
            form = create_ecju_create_confirmation_form()
            form.questions.append(HiddenField('question', request.POST.get('question')))
            return form_page(request, form)

    def _handle_ecju_query_confirmation_post(self, case_id, request):
        data = {'question': request.POST.get('question')}

        if request.POST.get('ecju_query_confirmation') == 'yes':
            ecju_query, status_code = post_ecju_query(request, case_id, data)

            if status_code != 201:
                return self._handle_ecju_query_form_errors(case_id, ecju_query, request)
            else:
                return redirect(reverse('cases:ecju_queries', kwargs={'pk': case_id}))
        elif request.POST.get('ecju_query_confirmation') == 'no':
            form = create_ecju_query_write_or_edit_form(reverse('cases:ecju_queries_add', kwargs={'pk': case_id}))

            return form_page(request, form, data=data)
        else:
            errors = {'ecju_query_confirmation': ['This field is required']}

            form = create_ecju_create_confirmation_form()
            form.questions.append(HiddenField('question', request.POST.get('question')))
            return form_page(request, form, errors=errors)

    def _handle_ecju_query_form_errors(self, case_id, ecju_query, request):
        errors = ecju_query.get('errors')
        errors = {error: message for error, message in errors.items()}
        form = create_ecju_query_write_or_edit_form(reverse('cases:ecju_queries_add', kwargs={'pk': case_id}))
        data = {'question': request.POST.get('question')}
        return form_page(request, form, data=data, errors=errors)


class ManageCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        statuses, status_code = get_statuses(request)

        if case['case']['type']['key'] == 'application':
            title = 'Manage ' + case.get('case').get('application').get('name')
        else:
            title = 'Manage CLC query case'

        context = {
            'data': case,
            'title': title,
            'statuses': statuses
        }
        return render(request, 'cases/manage.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        if case['case']['type']['key'] == 'application':
            application_id = case.get('case').get('application').get('id')
            data, status_code = put_applications(request, application_id, request.POST)
        else:
            clc_query_id = case['case']['clc_query']['id']
            data, status_code = put_clc_queries(request, clc_query_id, request.POST)

        if 'errors' in data:
            return redirect('/cases/' + case_id + '/manage')

        return redirect(reverse('cases:case', kwargs={'pk': case_id}))


class DecideCase(TemplateView):
    @has_permission(MAKE_FINAL_DECISIONS)
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

    @has_permission(MAKE_FINAL_DECISIONS)
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

        return redirect(reverse('cases:case', kwargs={'pk': case_id}))


class DenyCase(TemplateView):
    @has_permission(MAKE_FINAL_DECISIONS)
    def get(self, request, **kwargs):
        return form_page(request, denial_reasons_form())

    @has_permission(MAKE_FINAL_DECISIONS)
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


class AssignFlags(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case_data, status_code = get_case(request, case_id)
        case_level_team_flags_data, status_code = get_flags_case_level_for_team(request)
        case_flags = case_data.get('case').get('flags')
        case_level_team_flags = case_level_team_flags_data.get('flags')

        for flag in case_level_team_flags:
            for case_flag in case_flags:
                flag['selected'] = flag['id'] == case_flag['id']
                if flag['selected']:
                    break

        context = {
            'case': case_data,
            'case_level_team_flags': case_level_team_flags
        }
        return render(request, 'cases/case/case_flags.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        flags = request.POST.getlist('flags[]')

        response, status_code = put_case_flags(request, case_id, {'flags': flags})

        return redirect(reverse('cases:case', kwargs={'pk': case_id}))


class Documents(TemplateView):
    def get(self, request, **kwargs):
        """
        List all documents belonging to a case
        """
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        case_documents, status_code = get_case_documents(request, case_id)

        context = {
            'title': get_string('cases.manage.documents.title'),
            'case': case['case'],
            'case_documents': case_documents['documents'],
        }
        return render(request, 'cases/case/documents.html', context)


@method_decorator(csrf_exempt, 'dispatch')
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        get_case(request, case_id)

        form = attach_documents_form(reverse('cases:documents', kwargs={'pk': case_id}))

        return form_page(request, form, extra_data={'case_id': case_id})

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        case_id = str(kwargs['pk'])
        data = []

        files = request.FILES.getlist("file")
        if len(files) is not 1:
            return error_page(None, 'We had an issue uploading your files. Try again later.')
        file = files[0]
        data.append({
            'name': file.original_name,
            's3_key': file.name,
            'size': int(file.size / 1024) if file.size else 0,  # in kilobytes
            'description': request.POST['description'],
        })

        # Send LITE API the file information
        case_documents, status_code = post_case_documents(request, case_id, data)

        if 'errors' in case_documents:
            return error_page(None, 'We had an issue uploading your files. Try again later.')

        return redirect(reverse('cases:documents', kwargs={'pk': case_id}))


class Document(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        file_pk = str(kwargs['file_pk'])

        document, status_code = get_document(request, file_pk)
        original_file_name = document['document']['name']

        # Stream file
        def generate_file(result):
            for chunk in iter(lambda: result['Body'].read(settings.STREAMING_CHUNK_SIZE), b''):
                yield chunk

        s3 = s3_client()
        s3_key = document['document']['s3_key']
        s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
        _kwargs = {}
        if s3_response.get('ContentType'):
            _kwargs['content_type'] = s3_response['ContentType']
        response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
        response['Content-Disposition'] = f'attachment; filename="{original_file_name}"'
        return response

# May be added to a future story, so don't delete :)
# class DeleteDocument(TemplateView):
#     def get(self, request, **kwargs):
#         case_id = str(kwargs['pk'])
#         file_pk = str(kwargs['file_pk'])
#
#         case, status_code = get_case(request, case_id)
#         document, status_code = get_case_document(request, case_id, file_pk)
#         original_file_name = document['document']['name']
#
#         context = {
#             'title': 'Are you sure you want to delete this file?',
#             'description': original_file_name,
#             'case': case['case'],
#             'document': document['document'],
#             'page': 'cases/case/modals/delete_document.html',
#         }
#         return render(request, 'core/static.html', context)
#
#     def post(self, request, **kwargs):
#         case_id = str(kwargs['pk'])
#         file_pk = str(kwargs['file_pk'])
#
#         case, status_code = get_case(request, case_id)
#
#         # Delete the file on the API
#         delete_case_document(request, case_id, file_pk)
#
#
#
#         context = {
#             'title': 'Are you sure you want to delete this file?',
#             'description': original_file_name,
#             'case': case['case'],
#             'document': document['document'],
#             'page': 'cases/case/modals/delete_document.html',
#         }
#         return render(request, 'core/static.html', context)
