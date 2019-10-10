from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from lite_forms.generators import form_page, success_page
from lite_forms.submitters import submit_paged_form

from apply_for_a_licence.forms.initial import initial_questions
from conf.constants import STANDARD_LICENCE
from core.services import get_sites_on_draft, get_external_locations_on_draft
from drafts.services import get_third_parties, get_consignee_document, get_additional_documents
from drafts.services import post_drafts, get_draft, get_draft_goods, submit_draft, \
    delete_draft, get_draft_countries, get_draft_goods_types, get_ultimate_end_users, \
    get_end_user_document


class InitialQuestions(TemplateView):
    forms = initial_questions()

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_drafts)

        # If there are more forms to go through, continue
        if response:
            return response

        # If there is no response (no forms left to go through), go to the overview page
        return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': data['draft']['id']}))


def check_all_parties_have_a_document(parties):
    for party in parties:
        if not party['document']:
            return False
    return True


def get_licence_overview(request, kwargs, errors=None):
    draft_id = str(kwargs['pk'])
    data, status_code = get_draft(request, draft_id)

    if status_code != 200:
        # Wasn't able to get draft so redirecting to exporter hub
        return redirect(reverse('core:hub'))

    draft = data.get('draft')
    sites, _ = get_sites_on_draft(request, draft_id)
    external_locations, _ = get_external_locations_on_draft(request, draft_id)
    additional_documents, _ = get_additional_documents(request, draft_id)

    countries = {'countries': []}
    goods = {'goods': []}
    goodstypes = {'goods': []}
    ultimate_end_users = {'ultimate_end_users': []}
    ultimate_end_users_required = False
    third_parties = {'third_parties': []}
    end_user_document = None
    consignee_document = None
    countries_on_goods_types = False

    if draft['licence_type']['key'] == STANDARD_LICENCE:
        ultimate_end_users, _ = get_ultimate_end_users(request, draft_id)
        third_parties, _ = get_third_parties(request, draft_id)
        end_user = draft.get('end_user')
        consignee = draft.get('consignee')
        goods, _ = get_draft_goods(request, draft_id)

        if end_user:
            end_user_document, _ = get_end_user_document(request, draft_id)
            end_user_document = end_user_document.get('document')

        if consignee:
            consignee_document, _ = get_consignee_document(request, draft_id)
            consignee_document = consignee_document.get('document')

        for good in goods['goods']:
            if not good['good']['is_good_end_product']:
                ultimate_end_users_required = True
    else:
        goodstypes, _ = get_draft_goods_types(request, draft_id)
        countries, _ = get_draft_countries(request, draft_id)

        for good in goodstypes['goods']:
            if good['countries']:
                countries_on_goods_types = True

    context = {
        'title': 'Application Overview',
        'draft': draft,
        'sites': sites['sites'],
        'goods': goods['goods'],
        'countries': countries['countries'],
        'goodstypes': goodstypes['goods'],
        'external_locations': external_locations['external_locations'],
        'ultimate_end_users': ultimate_end_users['ultimate_end_users'],
        'ultimate_end_users_required': ultimate_end_users_required,
        'ultimate_end_users_documents_complete':
            check_all_parties_have_a_document(ultimate_end_users['ultimate_end_users']),
        'end_user_document': end_user_document,
        'consignee_document': consignee_document,
        'countries_on_goods_types': countries_on_goods_types,
        'third_parties': third_parties['third_parties'],
        'additional_documents': additional_documents['documents']
    }

    if errors:
        context['errors'] = errors

    return render(request, 'apply_for_a_licence/overview.html', context)


class Overview(TemplateView):
    def get(self, request, **kwargs):
        return get_licence_overview(request, kwargs)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = submit_draft(request, draft_id)

        if status_code != 200:
            return get_licence_overview(request, kwargs, data.get('errors'))

        return success_page(request,
                            title='Application submitted',
                            secondary_title='',
                            description='',
                            what_happens_next=[],
                            links={'Go to applications': reverse_lazy('applications:applications')})


# Delete Application
class DeleteApplication(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, _ = get_draft(request, draft_id)
        context = {
            'title': 'Are you sure you want to delete this application?',
            'draft': draft.get('draft'),
            'page': 'apply_for_a_licence/modals/cancel_application.html',
        }
        return render(request, 'core/static.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        delete_draft(request, draft_id)

        if request.GET.get('return') == 'drafts':
            return redirect(reverse_lazy('drafts:index') + '/?application_deleted=true')

        return redirect('/?application_deleted=true')
