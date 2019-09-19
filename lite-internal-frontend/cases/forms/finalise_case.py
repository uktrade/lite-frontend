from django.urls import reverse_lazy
from lite_forms.components import Form, TextInput, BackLink, DateInput


def approve_licence_form(case_id):
    return Form(
        title='Approve',
        questions=[
            DateInput(description='For example, 27 3 2007', title='When will the licence start?', prefix=''),
            TextInput(name='duration', description='This must be a whole number of months, such as 12', title='How long will it last?'),
        ],
        back_link=BackLink(url=reverse_lazy('cases:final_advice_view', kwargs={'pk': case_id}), text='Back to final advice'),
    )


def refuse_licence_form(case_id):
    return Form(
        title='Refuse',
        back_link=BackLink(url=reverse_lazy('cases:final_advice_view', kwargs={'pk': case_id}), text='Back to final advice'),
    )
