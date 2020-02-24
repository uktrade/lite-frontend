from lite_content.lite_internal_frontend import strings
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from lite_forms.generators import form_page, error_page
from lite_forms.submitters import submit_paged_form

from letter_templates.forms import add_letter_template
from letter_templates.helpers import get_template_content
from letter_templates.services import post_letter_template
from letter_templates.views.letter_paragraphs import get_order_paragraphs_page


class Add(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, add_letter_template(request).forms[0])

    @staticmethod
    def post(request):
        next_form, _ = submit_paged_form(request, add_letter_template(request), post_letter_template,)

        if next_form:
            return next_form

        template_content = get_template_content(request)
        return get_order_paragraphs_page(request, template_content)


class Create(TemplateView):
    @staticmethod
    def post(request):
        json = request.POST.copy()
        json["letter_paragraphs"] = request.POST.getlist("letter_paragraphs")
        json["case_types"] = request.POST.getlist("case_types[]")
        json["decisions"] = request.POST.getlist("decisions[]")
        response, status_code = post_letter_template(request, json)

        if status_code == 201:
            messages.success(request, strings.LetterTemplates.LetterTemplates.SUCCESSFULLY_CREATED_BANNER)

        else:
            error_messages = []
            errors = response["errors"]
            for field_errors in errors.values():
                for field_error in field_errors:
                    error_messages.append(field_error)

            return error_page(None, "; ".join(error_messages))

        return redirect("letter_templates:letter_templates")
