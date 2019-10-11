import logging

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from lite_forms.generators import form_page, error_page
from s3chunkuploader.file_handler import S3FileUploadHandler

from apply_for_a_licence.forms.end_user import attach_document_form, delete_document_confirmation_form
from apply_for_a_licence.services import add_document_data, download_document_from_s3
from core.builtins.custom_tags import get_string
from drafts.services import get_draft_application, post_ultimate_end_user_document, post_end_user_document, \
    get_ultimate_end_user_document, get_end_user_document, delete_ultimate_end_user_document, delete_end_user_document, \
    post_consignee_document, get_consignee_document, delete_consignee_document, post_third_party_document, \
    get_third_party_document, delete_third_party_document, post_additional_document, get_additional_document, \
    delete_additional_party_document

document_forms_paths = {
    'ultimate-end-user':
        {
            'homepage': 'apply_for_a_licence:ultimate_end_users',
            'strings': 'ultimate_end_user.documents',
            'description': False
        },
    'end-user':
        {
            'homepage': 'apply_for_a_licence:overview',
            'strings': 'end_user.documents',
            'description': False
        },
    'consignee':
        {
            'homepage': 'apply_for_a_licence:overview',
            'strings': 'consignee.documents',
            'description': False
        },
    'third-parties':
        {
            'homepage': 'apply_for_a_licence:third_parties',
            'strings': 'third_parties.documents',
            'description': False
        },
    'additional-document':
        {
            'homepage': 'apply_for_a_licence:additional_documents',
            'strings': 'additional_documents.documents',
            'description': True
        }
}


def get_page_content(path):
    if 'ultimate-end-user' in path:
        return document_forms_paths['ultimate-end-user']
    elif 'end-user' in path:
        return document_forms_paths['end-user']
    elif 'consignee' in path:
        return document_forms_paths['consignee']
    elif 'third-parties' in path:
        return document_forms_paths['third-parties']
    elif 'additional-document' in path:
        return document_forms_paths['additional-document']
    else:
        return None


def get_upload_page(path, draft_id):
    paths = get_page_content(path)

    if paths['description']:
        description_text = get_string(paths['strings'] + '.attach_documents.description_field_title')
    else:
        description_text = None

    return attach_document_form(draft_url=reverse(paths['homepage'], kwargs={'pk': draft_id}),
                                title=get_string(paths['strings'] + '.attach_documents.title'),
                                back_text=get_string(
                                    paths['strings'] + '.attach_documents.back_to_application_overview'),
                                return_later_text=get_string(paths['strings'] + '.save_end_user'),
                                description_text=description_text)


def get_homepage(request, draft_id):
    return redirect(reverse(get_page_content(request.path)['homepage'], kwargs={'pk': draft_id}))


def get_delete_confirmation_page(path, pk):
    paths = get_page_content(path)
    return delete_document_confirmation_form(
        overview_url=reverse(paths['homepage'], kwargs={'pk': pk}),
        back_link_text=get_string(paths['strings'] + '.attach_documents.back_to_application_overview')
    )


@method_decorator(csrf_exempt, 'dispatch')
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        _, status_code = get_draft_application(request, draft_id)
        if status_code == 200:
            form = get_upload_page(request.path, draft_id)
            return form_page(request, form, extra_data={'draft_id': draft_id})
        else:
            return error_page(None, get_string('drafts.draft_not_found'))

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))
        logging.info(self.request)
        draft_id = str(kwargs['pk'])
        data, error = add_document_data(request)

        if error:
            return error_page(None, get_string('end_user.documents.attach_documents.upload_error'))

        if 'ultimate-end-user' in request.path:
            _, status_code = post_ultimate_end_user_document(request, draft_id,
                                                                             str(kwargs['ueu_pk']), data)
        elif 'consignee' in request.path:
            _, status_code = post_consignee_document(request, draft_id, data)
        elif 'third-parties' in request.path:
            _, status_code = post_third_party_document(request, draft_id, str(kwargs['tp_pk']), data)
        elif 'end-user' in request.path:
            _, status_code = post_end_user_document(request, draft_id, data)
        elif 'additional-document' in request.path:
            _, status_code = post_additional_document(request, draft_id, data)
        else:
            return error_page(None, get_string('end_user.documents.attach_documents.upload_error'))

        if status_code == 201:
            return get_homepage(request, draft_id)
        else:
            return error_page(None, get_string('end_user.documents.attach_documents.upload_error'))


class DownloadDocument(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        if 'ultimate-end-user' in request.path:
            document, _ = get_ultimate_end_user_document(request, draft_id, str(kwargs['ueu_pk']))
        elif 'consignee' in request.path:
            document, _ = get_consignee_document(request, draft_id)
        elif 'third-parties' in request.path:
            document, _ = get_third_party_document(request, draft_id, str(kwargs['tp_pk']))
        elif 'end-user' in request.path:
            document, _ = get_end_user_document(request, draft_id)
        elif 'additional-document' in request.path:
            document, _ = get_additional_document(request, draft_id, str(kwargs['doc_pk']))
        else:
            return error_page(None, get_string('end_user.documents.attach_documents.download_error'))

        document = document['document']
        if document['safe']:
            return download_document_from_s3(document['s3_key'], document['name'])
        else:
            return error_page(None, get_string('end_user.documents.attach_documents.download_error'))


class DeleteDocument(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, get_delete_confirmation_page(request.path, str(kwargs['pk'])))

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        option = request.POST.get('delete_document_confirmation')
        if option is None:
            return form_page(request, get_delete_confirmation_page(request.path, str(kwargs['pk'])),
                             errors={'delete_document_confirmation': ['This field is required']})
        else:
            if option == 'yes':
                if 'ultimate-end-user' in request.path:
                    status_code = delete_ultimate_end_user_document(request, draft_id, str(kwargs['ueu_pk']))
                elif 'consignee' in request.path:
                    status_code = delete_consignee_document(request, draft_id)
                elif 'third-parties' in request.path:
                    status_code = delete_third_party_document(request, draft_id, str(kwargs['tp_pk']))
                elif 'end-user' in request.path:
                    status_code = delete_end_user_document(request, draft_id)
                elif 'additional-document' in request.path:
                    status_code = delete_additional_party_document(request, draft_id, str(kwargs['doc_pk']))
                else:
                    return error_page(None, get_string('end_user.documents.attach_documents.delete_error'))

                if status_code == 204:
                    return get_homepage(request, draft_id)
                else:
                    return error_page(None, get_string('end_user.documents.attach_documents.delete_error'))
            else:
                return get_homepage(request, draft_id)
