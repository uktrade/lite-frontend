from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.builtins.custom_tags import get_string
from drafts.services import get_draft, post_drafts, put_draft, delete_draft, submit_draft, get_draft_goods, \
    post_draft_preexisting_goods
from goods.services import get_goods, get_good
from libraries.forms.helpers import get_form_by_pk, get_next_form_after_pk
from new_application import forms
from new_application.services import get_units


def index(request):
    context = {
        'title': get_string('licences.apply_for_a_licence'),
        'service_uses': get_string('licences.use_this_service_to'),
    }
    return render(request, 'new_application/index.html', context)


def start(request):
    return redirect(reverse_lazy('new_application:form', kwargs={'pk': forms.section1.forms[0].pk}))


def form(request, pk):
    if request.method == 'POST':
        data = request.POST

        # Send data to API
        if request.GET.get('id'):
            response, status_code = put_draft(request, request.GET.get('id'), data)
        else:
            response, status_code = post_drafts(request, data)

        # If there are errors returned from LITE API, return and show them
        if 'errors' in response:
            page = get_form_by_pk(pk, forms.section1)
            context = {
                'title': page.title,
                'page': page,
                'errors': response['errors'],
                'data': data,
                'draft_id': request.GET.get('id'),
            }
            return render(request, 'form.html', context)

        # If a return query param is set, go there instead of the next form
        return_to = request.GET.get('return')

        if return_to == 'overview':
            return redirect(reverse_lazy('new_application:overview') + '?id=' + request.GET.get('id'))

        # Get the next form, if null go to overview
        next_form = get_next_form_after_pk(pk, forms.section1)
        if next_form:
            return redirect(reverse_lazy('new_application:form',
                                         kwargs={'pk': next_form.pk}) + '?id=' + str(response['draft']['id']))
        else:
            return redirect(reverse_lazy('new_application:overview') + '?id=' + request.GET.get('id'))

    elif request.method == 'GET':
        page = get_form_by_pk(pk, forms.section1)
        data = {}

        if request.GET.get('id'):
            data, status_code = get_draft(request, request.GET.get('id'))
            data = data['draft']

        context = {
            'title': page.title,
            'page': page,
            'data': data,
            'draft_id': request.GET.get('id'),
        }
        return render(request, 'form.html', context)


def overview(request):
    draft_id = request.GET.get('id')
    data, status_code = get_draft(request, request.GET.get('id'))

    context = {
        'title': 'Overview',
        'data': data,
        'sections': [forms.section1],
        'draft_id': draft_id,
    }
    return render(request, 'new_application/overview.html', context)


def submit(request):
    data, status_code = submit_draft(request, request.GET.get('id'))

    if status_code is not 201:
        raise Http404

    context = {
        'title': 'Application Submitted',
        'data': data,
    }
    return render(request, 'new_application/application_success.html', context)


def cancel(request):
    context = {
        'title': 'Are you sure you want to delete this application?',
        'draft_id': request.GET.get('id'),
    }
    return render(request, 'new_application/cancel_confirmation.html', context)


def cancel_confirm(request):
    delete_draft(request, request.GET.get('id'))

    if request.GET.get('return') == 'drafts':
        return redirect('/drafts?application_deleted=true')

    return redirect('/?application_deleted=true')


def goods(request):
    draft_id = request.GET.get('id')
    draft, status_code = get_draft(request, draft_id)
    data, status_code = get_draft_goods(request, draft_id)

    context = {
        'title': 'Application Goods',
        'draft_id': draft_id,
        'data': data,
        'draft': draft,
    }
    return render(request, 'new_application/goods/index.html', context)


def add_preexisting(request):
    draft_id = request.GET.get('id')
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
    }
    return render(request, 'new_application/goods/preexisting.html', context)


class AddPreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        good, status_code = get_good(request, str(kwargs['pk']))
        good = good.get('good')

        context = {
            'title': 'Add a pre-existing good to your application',
            'page': forms.preexisting_good_form(good.get('id'),
                                                good.get('description'),
                                                good.get('control_code'),
                                                good.get('part_number'),
                                                get_units(request)),
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        draft_id = request.GET.get('id')
        data, status_code = post_draft_preexisting_goods(request, draft_id, request.POST)

        if status_code != 201:
            good, status_code = get_good(request, str(kwargs['pk']))
            good = good.get('good')

            context = {
                'title': 'Add a pre-existing good to your application',
                'page': forms.preexisting_good_form(good.get('id'),
                                                    good.get('description'),
                                                    good.get('control_code'),
                                                    good.get('part_number'),
                                                    get_units(request)),
                'body': request.POST,
                'errors': data.get('errors'),
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('new_application:goods') + '?id=' + draft_id)
