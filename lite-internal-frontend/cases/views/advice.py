from django.contrib import messages
from django.http import Http404, HttpRequest
from django.middleware.csrf import rotate_token
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.advice import advice_recommendation_form
from cases.helpers import clean_advice
from cases.services import get_case, post_case_advice, get_case_advice
from core.services import get_denial_reasons
from libraries.forms.components import HiddenField
from libraries.forms.generators import form_page, error_page
from picklists.services import get_picklists


def add_hidden_advice_data(questions_list, data):
    questions_list.append(HiddenField('goods', data.getlist('goods')))
    questions_list.append(HiddenField('goods_types', data.getlist('goods_types')))
    questions_list.append(HiddenField('countries', data.getlist('countries')))
    questions_list.append(HiddenField('end_user', data.get('end_user', '')))
    questions_list.append(HiddenField('ultimate_end_users', data.getlist('ultimate_end_users')))
    return questions_list


class ViewAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(self.case_id)

        return super(ViewAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """
        advice, status_code = get_case_advice(request, self.case_id)

        context = {
            'case': self.case,
            'title': self.case.get('application').get('name'),
            'all_advice': advice['advice'],
        }
        return render(request, 'cases/case/advice-view.html', context)

    def post(self, request, **kwargs):
        rotate_token(request)

        data = request.POST

        # Validate at least one checkbox is checked
        if not len(data) > 1:
            return error_page(request, 'Select at least one good or destination to give advice on')

        # Add data to the form as hidden fields
        self.form.questions = add_hidden_advice_data(self.form.questions, data)

        return form_page(request, self.form)


class GiveAdvice(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        case, _ = get_case(request, case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(case_id)

        return super(GiveAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        data = request.POST

        # Validate at least one radiobutton is selected
        if not data.get('type'):
            # Add data to the error form as hidden fields
            self.form.questions = add_hidden_advice_data(self.form.questions, data)

            return form_page(request, self.form, errors={'type': ['Select a decision']})

        # Render the advice detail page
        proviso_picklist_items, status_code = get_picklists(request, 'proviso')
        advice_picklist_items, status_code = get_picklists(request, 'standard_advice')
        static_denial_reasons, status_code = get_denial_reasons(request, False)

        self.form = 'cases/case/give-advice.html'

        context = {
            'case': self.case,
            'title': 'Give advice',
            'type': data.get('type'),
            'proviso_picklist': proviso_picklist_items['picklist_items'],
            'advice_picklist': advice_picklist_items['picklist_items'],
            'static_denial_reasons': static_denial_reasons,
            # Add previous data
            'goods': data.get('goods'),
            'goods_types': data.get('goods_types'),
            'countries': data.get('countries'),
            'end_user': data.get('end_user'),
            'ultimate_end_users': data.get('ultimate_end_users'),
        }
        return render(request, self.form, context)


class GiveAdviceDetail(TemplateView):
    case_id = None
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']

        # If the advice type is not valid, raise a 404
        advice_type = kwargs['type']
        if advice_type not in ['approve', 'proviso', 'refuse', 'no_licence_required', 'not_applicable']:
            raise Http404

        return super(GiveAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        data = request.POST
        response, status_code = post_case_advice(request, self.case_id, data)

        if 'errors' in response:
            proviso_picklist_items, status_code = get_picklists(request, 'proviso')
            advice_picklist_items, status_code = get_picklists(request, 'standard_advice')
            static_denial_reasons, status_code = get_denial_reasons(request, False)

            data = clean_advice(data)

            context = {
                'case': self.case,
                'title': 'Error: Give advice',
                'type': data.get('type'),
                'proviso_picklist': proviso_picklist_items['picklist_items'],
                'advice_picklist': advice_picklist_items['picklist_items'],
                'static_denial_reasons': static_denial_reasons,
                # Add previous data
                'goods': data.get('goods'),
                'goods_types': data.get('goods_types'),
                'countries': data.get('countries'),
                'end_user': data.get('end_user'),
                'ultimate_end_users': data.get('ultimate_end_users'),
                'errors': response['errors'][0],
                'data': data,
            }
            return render(request, self.form, context)

        # Add success message
        messages.success(request, 'Your advice has been posted successfully')

        return redirect(reverse_lazy('cases:advice_view', kwargs={'pk': self.case_id}))
