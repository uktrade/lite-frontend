from django.shortcuts import render

from applications import services
from apply_for_a_licence.views import check_all_parties_have_a_document
from conf.constants import STANDARD_LICENCE
from core.services import get_sites_on_draft, get_external_locations_on_draft


def get_licence_overview(request, application, errors=None):
    application_id = application['id']

    # Add the editing type (if possible) to the context to make it easier to read/change in the future
    is_editing = application['status']['key'] == 'submitted' or application['status']['key'] == 'applicant_editing'
    edit_type = None
    if is_editing:
        edit_type = 'minor_edit' if application['status']['key'] == 'submitted' else 'major_edit'

    sites, _ = get_sites_on_draft(request, application_id)
    external_locations, _ = get_external_locations_on_draft(request, application_id)
    additional_documents, _ = services.get_additional_documents(request, application_id)

    countries = []
    goods = []
    goodstypes = []
    ultimate_end_users = []
    ultimate_end_users_required = False
    third_parties = []
    end_user_document = None
    consignee_document = None
    countries_on_goods_types = False

    if application['licence_type']['key'] == STANDARD_LICENCE:
        ultimate_end_users = services.get_ultimate_end_users(request, application_id)
        third_parties = services.get_third_parties(request, application_id)
        end_user = application.get('end_user')
        consignee = application.get('consignee')
        goods = services.get_application_goods(request, application_id)

        if end_user:
            end_user_document, _ = services.get_end_user_document(request, application_id)
            end_user_document = end_user_document.get('document')

        if consignee:
            consignee_document, _ = services.get_consignee_document(request, application_id)
            consignee_document = consignee_document.get('document')

        for good in goods:
            if not good['good']['is_good_end_product']:
                ultimate_end_users_required = True
    else:
        goodstypes = services.get_application_goods_types(request, application_id)
        countries = services.get_application_countries(request, application_id)

        for good in goodstypes:
            if good['countries']:
                countries_on_goods_types = True

    context = {
        'application': application,
        'is_editing': is_editing,
        'edit_type': edit_type,
        'sites': sites['sites'],
        'goods': goods,
        'countries': countries,
        'goodstypes': goodstypes,
        'external_locations': external_locations['external_locations'],
        'ultimate_end_users': ultimate_end_users,
        'ultimate_end_users_required': ultimate_end_users_required,
        'ultimate_end_users_documents_complete': check_all_parties_have_a_document(ultimate_end_users),
        'end_user_document': end_user_document,
        'consignee_document': consignee_document,
        'countries_on_goods_types': countries_on_goods_types,
        'third_parties': third_parties,
        'additional_documents': additional_documents['documents']
    }

    if errors:
        context['errors'] = errors

    return render(request, 'applications/edit.html', context)
