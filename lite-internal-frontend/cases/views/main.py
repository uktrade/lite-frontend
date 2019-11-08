from django.http import StreamingHttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from lite_forms.generators import error_page, form_page
from lite_forms.submitters import submit_single_form
from s3chunkuploader.file_handler import S3FileUploadHandler, s3_client

from cases.forms.attach_documents import attach_documents_form
from cases.forms.move_case import move_case_form
from cases.services import get_case, post_case_notes, put_application_status, get_activity, put_case, \
    put_end_user_advisory_query, _get_all_distinct_flags
from cases.services import post_case_documents, get_case_documents, get_document
from conf import settings
from conf.constants import DEFAULT_QUEUE_ID
from conf.settings import AWS_STORAGE_BUCKET_NAME
from core.builtins.custom_tags import get_string
from core.helpers import convert_dict_to_query_params
from core.services import get_user_permissions, get_statuses, get_user_case_notification
from queues.services import get_cases_search_data


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to that queue
        """
        case_type = request.GET.get('case_type')
        status = request.GET.get('status')
        sort = request.GET.get('sort')
        queue_id = request.GET.get('queue_id')

        # Page parameters
        params = {'page': int(request.GET.get('page', 1))}
        if queue_id:
            params['queue_id'] = queue_id
        if sort:
            params['sort'] = sort
        if status:
            params['status'] = status
        if case_type:
            params['case_type'] = case_type

        data = get_cases_search_data(request, convert_dict_to_query_params(params))

        context = {
            'title': data['results']['queue']['name'],
            'data': data,
            'queue': data['results']['queue'],
            'page': params.pop('page'),
            'params': params,
            'params_str': convert_dict_to_query_params(params)
        }

        return render(request, 'cases/index.html', context)

    def post(self, request, **kwargs):
        """
        Assign users depending on what cases were selected
        """
        queue_id = request.GET.get('queue_id', DEFAULT_QUEUE_ID)
        return redirect(reverse('queues:case_assignments', kwargs={'pk': queue_id}) + '?cases=' + ','.join(
            request.POST.getlist('cases')))


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)
        activity = get_activity(request, case_id)
        permissions = get_user_permissions(request)
        queue_id = request.GET.get('queue_id')
        queue_name = request.GET.get('queue_name')

        case['all_flags'] = _get_all_distinct_flags(case)

        context = {
            'title': 'Case',
            'case': case,
            'activity': activity,
            'permissions': permissions,
        }
        if queue_id:
            context['queue_id'] = queue_id
        if queue_name:
            context['queue_name'] = queue_name

        if case['type']['key'] == 'end_user_advisory_query':
            return render(request, 'cases/case/queries/end_user_advisory.html', context)
        elif case['type']['key'] == 'clc_query':
            context['good'] = case['query']['good']
            return render(request, 'cases/case/queries/clc-query-case.html', context)
        elif case['type']['key'] == 'application':
            context['title'] = case.get('application').get('name')
            context['notification'] = get_user_case_notification(request, case_id)
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
        case = get_case(request, case_id)
        activity, _ = get_activity(request, case_id)
        permissions = get_user_permissions(request)

        context = {
            'data': case,
            'title': case.get('application').get('name'),
            'activity': activity.get('activity'),
            'permissions': permissions,
            'edit_case_flags': get_string('cases.case.edit_case_flags')
        }
        return render(request, 'cases/case/user-advice-view.html', context)


class ManageCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)
        statuses, _ = get_statuses(request)

        reduced_statuses = {'statuses': [x for x in statuses['statuses'] if
                                         (x['status'] != 'finalised' and x['status'] != 'applicant_editing')]}

        if case['type']['key'] == 'application':
            title = 'Manage ' + case.get('application').get('name')
        elif case['query']['end_user']:
            title = 'Manage End User Advisory'
        else:
            title = 'Manage CLC query case'

        context = {
            'case': case,
            'title': title,
            'statuses': reduced_statuses
        }
        return render(request, 'cases/case/change-status.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)

        if case['type']['key'] == 'application':
            application_id = case.get('application').get('id')
            put_application_status(request, application_id, request.POST)
        elif case['type']['key'] == 'end_user_advisory_query':
            query_id = case.get('query').get('id')
            put_end_user_advisory_query(request, query_id, request.POST)
        else:
            raise Http404

        return redirect(reverse('cases:case', kwargs={'pk': case_id}))


class MoveCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)

        return form_page(request,
                         move_case_form(request, reverse('cases:case', kwargs={'pk': case_id})),
                         data=case)

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


class Documents(TemplateView):
    def get(self, request, **kwargs):
        """
        List all documents belonging to a case
        """
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)
        case_documents, _ = get_case_documents(request, case_id)

        context = {
            'title': get_string('cases.manage.documents.title'),
            'case': case,
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
            'size': int(file.size // 1024) if file.size else 0,  # in kilobytes
            'description': request.POST['description'],
        })

        # Send LITE API the file information
        case_documents, _ = post_case_documents(request, case_id, data)

        if 'errors' in case_documents:
            return error_page(None, 'We had an issue uploading your files. Try again later.')

        return redirect(reverse('cases:documents', kwargs={'pk': case_id}))


class Document(TemplateView):
    def get(self, request, **kwargs):
        file_pk = str(kwargs['file_pk'])

        document, _ = get_document(request, file_pk)
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
#         case = get_case(request, case_id)
#         document, status_code = get_case_document(request, case_id, file_pk)
#         original_file_name = document['document']['name']
#
#         context = {
#             'title': 'Are you sure you want to delete this file?',
#             'description': original_file_name,
#             'case': case,
#             'document': document['document'],
#             'page': 'cases/case/modals/delete_document.html',
#         }
#         return render(request, 'core/static.html', context)
#
#     def post(self, request, **kwargs):
#         case_id = str(kwargs['pk'])
#         file_pk = str(kwargs['file_pk'])
#
#         case = get_case(request, case_id)
#
#         # Delete the file on the API
#         delete_case_document(request, case_id, file_pk)
#
#
#
#         context = {
#             'title': 'Are you sure you want to delete this file?',
#             'description': original_file_name,
#             'case': case,
#             'document': document['document'],
#             'page': 'cases/case/modals/delete_document.html',
#         }
#         return render(request, 'core/static.html', context)
