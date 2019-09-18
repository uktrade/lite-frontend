from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import error_page, form_page

from cases.forms.advice import advice_recommendation_form
from cases.helpers import clean_advice, check_matching_advice, add_hidden_advice_data
from cases.services import get_case, post_case_advice, get_case_advice
from core.services import get_denial_reasons
from picklists.services import get_picklists


class ViewAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case = get_case(request, self.case_id)
        self.case = case
        self.form = advice_recommendation_form(self.case_id)

        return super(ViewAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """
        advice, _ = get_case_advice(request, self.case_id)

        context = {
            'case': self.case,
            'title': self.case.get('application').get('name'),
            'all_advice': advice['advice'],
        }
        return render(request, 'cases/case/advice-view.html', context)

    def post(self, request, **kwargs):

        advice, _ = get_case_advice(request, self.case_id)
        selected_advice_data = request.POST
        pre_data = check_matching_advice(request.user.lite_api_user_id, advice['advice'], selected_advice_data)

        # Validate at least one checkbox is checked
        if not len(selected_advice_data) > 0:
            return error_page(request, 'Select at least one good or destination to give advice on')

        # Add data to the form as hidden fields
        self.form.questions = add_hidden_advice_data(self.form.questions, selected_advice_data)

        return form_page(request, self.form, data=pre_data)


class GiveAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case = get_case(request, self.case_id)
        self.case = case
        self.form = advice_recommendation_form(self.case_id)

        return super(GiveAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        selected_advice_data = request.POST
        advice, _ = get_case_advice(request, self.case_id)
        pre_data = check_matching_advice(request.user.lite_api_user_id, advice['advice'], selected_advice_data)

        if pre_data and not str(selected_advice_data['type']) in str(pre_data['type']):
            pre_data = None

        # Validate at least one radiobutton is selected
        if not selected_advice_data.get('type'):
            # Add data to the error form as hidden fields
            self.form.questions = add_hidden_advice_data(self.form.questions, selected_advice_data)

            return form_page(request, self.form, errors={'type': ['Select a decision']})

        # Render the advice detail page
        proviso_picklist_items = get_picklists(request, 'proviso')
        advice_picklist_items = get_picklists(request, 'standard_advice')
        static_denial_reasons, _ = get_denial_reasons(request, False)

        self.form = 'cases/case/give-advice.html'

        context = {
            'case': self.case,
            'title': 'Give advice',
            'type': selected_advice_data.get('type'),
            'proviso_picklist': proviso_picklist_items['picklist_items'],
            'advice_picklist': advice_picklist_items['picklist_items'],
            'static_denial_reasons': static_denial_reasons,
            # Add previous data
            'goods': selected_advice_data.get('goods'),
            'goods_types': selected_advice_data.get('goods_types'),
            'countries': selected_advice_data.get('countries'),
            'end_user': selected_advice_data.get('end_user'),
            'ultimate_end_users': selected_advice_data.get('ultimate_end_users'),
            'third_parties': selected_advice_data.get('third_parties'),
            'consignee': selected_advice_data.get('consignee'),
            'data': pre_data,
        }
        return render(request, self.form, context)


class GiveAdviceDetail(TemplateView):
    case_id = None
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case = get_case(request, self.case_id)
        self.case = case

        # If the advice type is not valid, raise a 404
        advice_type = kwargs['type']
        if advice_type not in ['approve', 'proviso', 'refuse', 'no_licence_required', 'not_applicable']:
            raise Http404

        return super(GiveAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        data = request.POST
        response, _ = post_case_advice(request, self.case_id, data)

        if 'errors' in response:
            proviso_picklist_items = get_picklists(request, 'proviso')
            advice_picklist_items = get_picklists(request, 'standard_advice')
            static_denial_reasons, _ = get_denial_reasons(request, False)

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
                'third_parties': data.get('third_parties'),
                'consignee': data.get('consignee'),
                'errors': response['errors'][0],
                'data': data,
            }
            return render(request, self.form, context)

        # Add success message
        messages.success(request, 'Your advice has been posted successfully')

        return redirect(reverse_lazy('cases:advice_view', kwargs={'pk': self.case_id}))
