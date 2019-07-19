from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler, s3_client, UploadFailed

from cases.forms.attach_documents import attach_documents_form
from cases.forms.denial_reasons import denial_reasons_form
from cases.forms.move_case import move_case_form
from cases.forms.record_decision import record_decision_form
from cases.services import post_case_documents, get_case_documents, get_case_document
from conf import settings
from conf.settings import env, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, \
    S3_DOWNLOAD_LINK_EXPIRY_SECONDS
from core.builtins.custom_tags import get_string
from cases.services import get_case, post_case_notes, put_applications, get_activity, put_case, put_clc_queries
from conf.constants import DEFAULT_QUEUE_ID, MAKE_FINAL_DECISIONS
from conf.decorators import has_permission
from core.services import get_queue, get_queues, get_user_permissions
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
        return redirect(reverse('queues:case_assignments', kwargs={'pk': queue_id}) + '?cases=' + ','.join(
            request.POST.getlist('cases')))


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        activity, status_code = get_activity(request, case_id)
        permissions = get_user_permissions(request)

        if case['case']['is_clc']:
            case_id = str(kwargs['pk'])
            case, status_code = get_case(request, case_id)

            context = {
                'title': 'Case',
                'data': case,
            }
            return render(request, 'cases/case/clc-query-case.html', context)

        context = {
            'data': case,
            'title': case.get('case').get('application').get('name'),
            'activity': activity.get('activity'),
            'permissions': permissions,
        }
        return render(request, 'cases/case/application-case.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:
            error = response.get('errors').get('text')[0]
            error = error.replace('This field', 'Case note')
            error = error.replace('this field', 'the case note')  # TODO: Move to API
            return error_page(request, error)

        return redirect(reverse('cases:case', kwargs={'pk': case_id}) + '#case_notes')


class ManageCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        if not case['case']['is_clc']:
            context = {
                'data': case,
                'title': 'Manage ' + case.get('case').get('application').get('name'),
            }
        else:
            context = {
                'data': case,
                'title': 'Manage CLC query case',
            }

        return render(request, 'cases/manage.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)

        if not case['case']['is_clc']:
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


class Documents(TemplateView):
    def get(self, request, **kwargs):
        """
        List all documents belonging to a case
        """
        case_id = str(kwargs['pk'])
        case, status_code = get_case(request, case_id)
        documents, status_code = get_case_documents(request, case_id)

        context = {
            'title': get_string('cases.manage.documents.title'),
            'case': case['case'],
            'documents': documents['documents'],
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

        get_case(request, case_id)
        document, status_code = get_case_document(request, case_id, file_pk)
        original_file_name = document['document']['name']

        # Stream file
        def generate_file(result):
            for chunk in iter(lambda: result['Body'].read(settings.STREAMING_CHUNK_SIZE), b''):
                yield chunk

        s3 = s3_client()
        s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_pk)
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
