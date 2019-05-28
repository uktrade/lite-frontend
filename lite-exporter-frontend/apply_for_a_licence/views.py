from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apply_for_a_licence import forms
from core.builtins.custom_tags import get_string
from core.services import get_units, post_sites_on_draft, get_sites_on_draft
from drafts.services import post_drafts, get_draft, get_draft_goods, post_draft_preexisting_goods, submit_draft, \
    delete_draft
from goods.services import get_goods, get_good
from libraries.forms.components import HiddenField, ArrayQuestion, Form, InputType
from libraries.forms.helpers import get_form_by_pk, get_next_form_after_pk, nest_data, remove_unused_errors, \
    success_page
from sites.services import get_sites


def create_persistent_bar(draft):
    return {
        'caption': 'Currently viewing:',
        'text': draft.get('name'),
        'url': reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft.get('id')}),
    }


class StartApplication(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': get_string('licences.apply_for_a_licence'),
            'service_uses': get_string('licences.use_this_service_to'),
        }
        return render(request, 'apply_for_a_licence/index.html', context)


class InitialQuestions(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'page': forms.initial_questions.forms[0],
            'title': forms.initial_questions.forms[0].title,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data = request.POST.copy()

        # Get the next form based off form_pk
        current_form = get_form_by_pk(data.get('form_pk'), forms.initial_questions)
        next_form = get_next_form_after_pk(data.get('form_pk'), forms.initial_questions)

        # Remove form_pk and CSRF from POST data as the new form will replace them
        del data['form_pk']
        del data['csrfmiddlewaretoken']

        # Post the data to the validator and check for errors
        nested_data = nest_data(data)
        validated_data, status_code = post_drafts(request, nested_data)

        if 'errors' in validated_data:
            validated_data['errors'] = remove_unused_errors(validated_data['errors'], current_form)

            # If there are errors in the validated data, take the user back
            if len(validated_data['errors']) is not 0:
                context = {
                    'page': current_form,
                    'title': current_form.title,
                    'errors': validated_data['errors'],
                    'data': data,
                }
                return render(request, 'form.html', context)

        # If there aren't any forms left to go through, submit all the data and go to the overview page
        if next_form is None:
            draft_pk = validated_data['draft']['id']
            return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_pk}))

        # Add existing post data to new form as hidden fields
        for key, value in data.items():
            next_form.questions.append(
                HiddenField(key, value)
            )

        # Go to the next page
        context = {
            'page': next_form,
            'title': next_form.title,
        }
        return render(request, 'form.html', context)


class Overview(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_draft(request, str(kwargs['pk']))

        context = {
            'title': 'Draft Overview',
            'draft': data.get('draft'),
            'persistent_bar': create_persistent_bar(data.get('draft')),
        }
        return render(request, 'apply_for_a_licence/overview.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = submit_draft(request, draft_id)

        if status_code is not 201:
            draft, status_code = get_draft(request, draft_id)

            context = {
                'title': 'Draft Overview',
                'draft': draft.get('draft'),
                'persistent_bar': create_persistent_bar(draft.get('draft')),
                'errors': data.get('errors'),
            }
            return render(request, 'apply_for_a_licence/overview.html', context)

        return success_page(request,
                            title='Application submitted',
                            secondary_title='',
                            description='',
                            what_happens_next=[],
                            links={
                                'Go to applications': reverse_lazy('applications:applications')
                            })


# Goods

class DraftGoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        data, status_code = get_draft_goods(request, draft_id)

        context = {
            'title': 'Application Goods',
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/goods/index.html', context)


class GoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        description = request.GET.get('description', '')
        part_number = request.GET.get('part_number', '')
        data, status_code = get_goods(request, {'description': description,
                                                'part_number': part_number})

        context = {
            'title': 'Goods',
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
            'description': description,
            'part_number': part_number,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/goods/preexisting.html', context)


class AddPreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        good, status_code = get_good(request, str(kwargs['good_pk']))
        good = good.get('good')

        context = {
            'title': 'Add a pre-existing good to your application',
            'page': forms.preexisting_good_form(good.get('id'),
                                                good.get('description'),
                                                good.get('control_code'),
                                                good.get('part_number'),
                                                get_units(request)),
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        data, status_code = post_draft_preexisting_goods(request, draft_id, request.POST)

        if status_code != 201:
            good, status_code = get_good(request, str(kwargs['good_pk']))
            good = good.get('good')

            context = {
                'title': 'Add a pre-existing good to your application',
                'page': forms.preexisting_good_form(good.get('id'),
                                                    good.get('description'),
                                                    good.get('control_code'),
                                                    good.get('part_number'),
                                                    get_units(request)),
                'persistent_bar': create_persistent_bar(draft.get('draft')),
                'data': request.POST,
                'errors': data.get('errors'),
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('apply_for_a_licence:goods', kwargs={'pk': draft_id}))


# Delete Application


class DeleteApplication(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        context = {
            'title': 'Are you sure you want to delete this application?',
            'draft_id': draft_id,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/cancel_confirmation.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        delete_draft(request, draft_id)

        if request.GET.get('return') == 'drafts':
            return redirect(reverse_lazy('drafts:index') + '/?application_deleted=true')

        return redirect('/?application_deleted=true')


# Sites


class Sites(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        response, status_code = get_sites_on_draft(request, draft_id)

        # Create the form
        sites_form = Form(title='Where are your goods located?',
                          description='Select all sites that apply.',
                          questions=[
                              ArrayQuestion('', '', InputType.CHECKBOXES, 'sites', get_sites(request, True))
                          ],
                          default_button_name='Save and continue')

        context = {
            'title': sites_form.title,
            'draft_id': draft_id,
            'page': sites_form,
            'data': response,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)

        data = {
            'sites': request.POST.getlist('sites')
        }

        response, status_code = post_sites_on_draft(request, draft_id, data)

        if status_code != 201:
            draft_id = request.GET.get('id')

            # Create the form
            sites_form = Form(title='Where are your goods located?',
                              description='Select all sites that apply.',
                              questions=[
                                  ArrayQuestion('', '', InputType.CHECKBOXES, 'sites', get_sites(request, True))
                              ],
                              default_button_name='Save and continue')

            context = {
                'title': sites_form.title,
                'draft_id': draft_id,
                'page': sites_form,
                'errors': response.get('errors'),
                'persistent_bar': create_persistent_bar(draft.get('draft')),
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_id}))
