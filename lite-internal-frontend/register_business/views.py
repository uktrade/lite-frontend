from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from lite_forms.components import HiddenField
from lite_forms.generators import form_page, success_page
from lite_forms.helpers import get_form_by_pk, get_next_form_after_pk, nest_data, flatten_data

from organisations.services import post_organisations
from register_business import forms


class RegisterBusiness(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.register_business_forms().forms[0])

    def post(self, request, **kwargs):
        data = request.POST.copy()
        register_business_forms = forms.register_business_forms()

        # Get the next form based off form_pk
        current_form = get_form_by_pk(data.get('form_pk'), register_business_forms)
        next_form = get_next_form_after_pk(data.get('form_pk'), register_business_forms)

        # Remove form_pk and CSRF from POST data as the new form will replace them
        del data['form_pk']
        del data['csrfmiddlewaretoken']

        # Post the data to the validator and check for errors
        nested_data = nest_data(data)
        validated_data, status_code = post_organisations(request, nested_data)

        if 'errors' in validated_data:
            for key, value in validated_data.get('errors').copy().items():
                if value == ['This field is required.']:
                    del validated_data.get('errors')[key]

            # If there are errors in the validated data, take the user back
            if len(validated_data['errors']) is not 0:

                # TODO: Clean up this code
                # Add hidden fields to the current form
                for key, value in data.items():
                    exists = False

                    for question in current_form.questions:
                        if hasattr(question, 'name'):
                            if question.name == key:
                                exists = True
                                continue

                    if not exists:
                        current_form.questions.append(
                            HiddenField(key, value)
                        )

                context = {
                    'page': current_form,
                    'title': current_form.title,
                    'errors': flatten_data(validated_data['errors']),
                    'data': data,
                }
                return render(request, 'form.html', context)

        # If there aren't any forms left to go through, submit all the data and go to a success page
        if next_form is None:
            return success_page(request,
                                title='Organisation Registered',
                                secondary_title=nested_data.get('name') + ' registered successfully',
                                description='',
                                what_happens_next=[],
                                links={
                                    'Go to organisations': reverse('organisations:organisations')
                                })

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
