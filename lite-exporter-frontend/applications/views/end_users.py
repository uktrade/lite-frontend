from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page, error_page
from lite_forms.submitters import submit_paged_form

from applications.forms.end_user import new_end_user_forms
from applications.services import get_application, post_end_user, get_ultimate_end_users, \
    post_ultimate_end_user, delete_ultimate_end_user, delete_end_user
from conf.constants import STANDARD_LICENCE


class EndUser(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, new_end_user_forms().forms[0])

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        response, _ = submit_paged_form(request, new_end_user_forms(), post_end_user, object_pk=draft_id)

        # If there are more forms to go through, continue
        if response:
            return response

        draft = get_application(request, draft_id)

        if draft.get('licence_type').get('key') == STANDARD_LICENCE:
            return redirect(reverse_lazy('applications:end_user_attach_document', kwargs={'pk': draft_id}))
        else:
            return redirect(reverse_lazy('applications:edit', kwargs={'pk': draft_id}))


class RemoveEndUser(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        status_code = delete_end_user(request, application_id)

        if status_code != 204:
            return error_page(request, 'Unexpected error removing end user')

        return redirect(reverse_lazy('applications:edit', kwargs={'pk': application_id}))


class UltimateEndUsers(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
        ultimate_end_users = get_ultimate_end_users(request, application_id)

        context = {
            'application': application,
            'ultimate_end_users': ultimate_end_users,
        }
        return render(request, 'applications/parties/ultimate_end_users.html', context)


class AddUltimateEndUser(TemplateView):
    draft_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs['pk'])
        self.form = new_end_user_forms()

        return super(AddUltimateEndUser, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.form, post_ultimate_end_user, object_pk=self.draft_id)

        if response:
            return response

        return redirect(reverse_lazy('applications:ultimate_end_user_attach_document',
                                     kwargs={'pk': self.draft_id, 'ueu_pk': data['ultimate_end_user']['id']}))


class RemoveUltimateEndUser(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        ueu_pk = str(kwargs['ueu_pk'])
        delete_ultimate_end_user(request, draft_id, ueu_pk)
        return redirect(reverse_lazy('applications:ultimate_end_users', kwargs={'pk': draft_id}))
