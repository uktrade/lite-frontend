from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from letter_templates.forms import edit_letter_template
from letter_templates.services import get_letter_template, put_letter_template, get_letter_paragraphs
from picklists.services import get_picklists


class EditTemplate(TemplateView):
    def get(self, request, **kwargs):
        letter_template = get_letter_template(request, str(kwargs['pk']))
        return form_page(request, edit_letter_template(letter_template), data=letter_template)

    @staticmethod
    def post(request, **kwargs):
        letter_template_id = str(kwargs['pk'])
        letter_template = get_letter_template(request, letter_template_id)

        # Override case restrictions to use getlist
        edited_letter_template_data = request.POST.copy()
        edited_letter_template_data['restricted_to'] = edited_letter_template_data.getlist('restricted_to')

        response = submit_single_form(request,
                                      edit_letter_template(letter_template),
                                      put_letter_template,
                                      object_pk=letter_template_id,
                                      override_data=edited_letter_template_data)[0]

        if response:
            return response

        return redirect(reverse('letter_templates:letter_template', kwargs={'pk': letter_template_id}))


class EditParagraphs(TemplateView):
    def get(self, request, **kwargs):
        letter_template = get_letter_template(request,  str(kwargs['pk']))

        if kwargs.get('override_paragraphs'):
            letter_template['letter_paragraphs'] = kwargs.get('override_paragraphs')

        letter_paragraphs = get_letter_paragraphs(request, letter_template['letter_paragraphs'])
        letter_paragraphs = self.sort_letter_paragraphs(letter_paragraphs, letter_template['letter_paragraphs'])

        context = {
            'letter_template': letter_template,
            'letter_paragraphs': letter_paragraphs
        }
        return render(request, 'letter_templates/edit_letter_paragraphs.html', context)

    @staticmethod
    def sort_letter_paragraphs(paragraphs, ids):
        """Order a list of letter paragraphs in the same order as a list of IDs."""
        paragraphs_by_id = {p["id"]: p for p in paragraphs}
        return [paragraphs_by_id[id] for id in ids if id in paragraphs_by_id]

    @staticmethod
    def _add_letter_paragraph(request, existing_paragraphs):
        all_letter_paragraphs = get_picklists(request, 'letter_paragraph')
        context = {
            'letter_paragraphs': [paragraph for paragraph in all_letter_paragraphs['picklist_items'] if
                                  paragraph['id'] not in existing_paragraphs],
            'existing_letter_paragraphs': existing_paragraphs
        }
        return render(request, 'letter_templates/add_letter_paragraphs.html', context)

    def post(self, request, **kwargs):
        letter_template_id = str(kwargs['pk'])
        action = request.POST.get('action')
        existing_paragraphs = request.POST.getlist('letter_paragraphs')

        if action == 'add_letter_paragraph':
            return self._add_letter_paragraph(request, existing_paragraphs)

        elif action == 'return_to_preview':
            return self.get(request, override_paragraphs=request.POST.getlist('letter_paragraphs'), **kwargs)

        elif 'delete' in action:
            pk_to_delete = action.split('.')[1]
            existing_paragraphs.remove(pk_to_delete)
            return self.get(request, override_paragraphs=existing_paragraphs, **kwargs)

        put_letter_template(request, letter_template_id,
                            {'letter_paragraphs': request.POST.getlist('letter_paragraphs')})
        return redirect(reverse('letter_templates:letter_template', kwargs={'pk': letter_template_id}))
