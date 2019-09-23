from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from apply_for_a_licence.forms.end_user import new_consignee_forms
from apply_for_a_licence.forms.third_party import third_party_forms, option_list
from drafts.services import post_third_party, get_third_parties, delete_third_party, post_consignee, get_draft


class AddThirdParty(TemplateView):
    draft_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs['pk'])
        draft, _ = get_draft(request, self.draft_id)
        self.form = third_party_forms(draft.get('draft').get('export_type'))

        return super(AddThirdParty, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.form, post_third_party, pk=self.draft_id)

        if response:
            return response

        return redirect(reverse_lazy('apply_for_a_licence:third_party_attach_document',
                                     kwargs={'pk': self.draft_id, 'tp_pk': data['third_party']['id']}))


class ThirdParties(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, _ = get_third_parties(request, draft_id)

        context = {
            'third_parties': data['third_parties'],
            'draft_id': draft_id,
            'third_party_types': option_list.values(),
            'add_link': 'apply_for_a_licence:add_third_party',
            'download_document_link': 'apply_for_a_licence:third_party_download_document',
            'delete_document_link': 'apply_for_a_licence:third_party_delete_document',
            'attach_document_link': 'apply_for_a_licence:third_party_attach_document',
            'delete_link': 'apply_for_a_licence:remove_third_party',
            'title': 'Third Parties'
        }

        return render(request, 'apply_for_a_licence/parties/third_parties.html', context)


class RemoveThirdParty(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        ueu_pk = str(kwargs['ueu_pk'])
        delete_third_party(request, draft_id, ueu_pk)
        return redirect(reverse_lazy('apply_for_a_licence:third_parties', kwargs={'pk': draft_id}))


class Consignee(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, new_consignee_forms().forms[0])

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        response, _ = submit_paged_form(request, new_consignee_forms(), post_consignee, pk=draft_id)

        # If there are more forms to go through, continue
        if response:
            return response

        return redirect(reverse_lazy('apply_for_a_licence:consignee_attach_document', kwargs={'pk': draft_id}))
