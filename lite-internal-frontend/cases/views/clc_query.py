from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.components import HiddenField
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from cases.forms.goods_flags import flags_form
from cases.forms.respond_to_clc_query import respond_to_clc_query_form
from cases.services import get_case, put_control_list_classification_query, put_flag_assignments
from core.services import get_user_permissions
from flags.services import get_goods_flags
from picklists.services import get_picklist_item


class Respond(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        self.case = get_case(request, case_id)
        self.form = respond_to_clc_query_form(request, self.case)

        permissions = get_user_permissions(request)
        if 'REVIEW_GOODS' not in permissions:
            return redirect(reverse_lazy('cases:case', kwargs={'pk': case_id}))

        return super(Respond, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        # If 'set-flags' take them to the goods flags page
        if request.POST.get('action') == 'set-flags':
            form = flags_form(
                flags=get_goods_flags(request, True),
                level='goods',
                origin='response',
                url='#'
            )

            form.questions.append(HiddenField('is_good_controlled', request.POST['is_good_controlled']))
            form.questions.append(HiddenField('control_code', request.POST.get('control_code')))
            form.questions.append(HiddenField('report_summary', request.POST['report_summary']))
            form.questions.append(HiddenField('comment', request.POST['comment']))

            form.post_url = reverse_lazy('cases:respond_to_clc_query_flags', kwargs={'pk': self.case['id']})
            return form_page(request, form, data={'flags': self.case['query']['good']['flags']})

        if request.POST.get('action') != 'change':
            form_data = request.POST.copy()

            if request.POST.get('report_summary') == 'None':
                del form_data['report_summary']

            response, response_data = submit_single_form(request,
                                                self.form,
                                                put_control_list_classification_query,
                                                pk=str(self.case['query']['id']),
                                                override_data=form_data)

            if response:
                return response
            response_data = response_data['control_list_classification_query']
        # If validate only is removed (therefore the user is on the overview page
        # already) go back to the case and show a success message
        if not request.POST.get('validate_only'):
            if request.POST.get('action') == 'change':
                return form_page(request, self.form, data=request.POST)

            return redirect(reverse_lazy('cases:case', kwargs={'pk': self.case['id']}))

        # Remove validate only key and go to overview page
        data = request.POST.copy()

        if data.get('validate_only') and data.get('report_summary'):
            report_summary = get_picklist_item(request, data['report_summary'])
        else:
            report_summary = {'text': ''}

        if response_data['is_good_controlled'] == 'no':
            response_data.pop('control_code')

        context = {
            'title': 'Response Overview',
            'data': response_data,
            'case': self.case,
            'report_summary': report_summary
        }
        return render(request, 'cases/case/clc_query_overview.html', context)


class RespondFlags(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case = get_case(request, str(kwargs['pk']))
        self.form = flags_form(
            flags=get_goods_flags(request, True),
            level='goods',
            origin='response',
            url='#'
        )
        self.form.post_url = reverse_lazy('cases:respond_to_clc_query_flags', kwargs={'pk': self.case['id']})

        return super(RespondFlags, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        put_flag_assignments(request,
                             {
                                 'level': 'Goods',
                                 'objects': self.case['query']['good']['id'],
                                 'flags': request.POST.getlist('flags'),
                                 'note': request.POST.get('note')
                             })

        context = {
            'title': 'Response Overview',
            'data': request.POST,
            'case': get_case(request, str(kwargs['pk'])),  # Do another pull of case as case flags have changed
            'report_summary': get_picklist_item(request, request.POST['report_summary'])
        }
        return render(request, 'cases/case/clc_query_overview.html', context)
