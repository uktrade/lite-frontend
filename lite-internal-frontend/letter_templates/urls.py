from django.urls import path

from conf.constants import Permission
from core.helpers import decorate_patterns_with_permission
from letter_templates.views import edit, letter_paragraphs, view, create

app_name = "letter_templates"

urlpatterns = [
    path("", view.LetterTemplatesList.as_view(), name="letter_templates"),
    path("<uuid:pk>/", view.LetterTemplateDetail.as_view(), name="letter_template"),
    path("<uuid:pk>/edit/", edit.EditTemplate.as_view(), name="edit"),
    path("<uuid:pk>/edit-paragraphs/", edit.EditParagraphs.as_view(), name="edit_letter_paragraphs"),
    # Create letter templates
    # ex: /letter-templates/add/
    path("add/", create.Add.as_view(), name="add"),
    # ex: /letter-templates/add/letter-paragraphs/
    path("add/letter-paragraphs/", letter_paragraphs.LetterParagraphs.as_view(), name="letter_paragraphs"),
    # ex: /letter-templates/create/
    path("create/", create.Create.as_view(), name="create"),
]

url_patterns = decorate_patterns_with_permission(urlpatterns, Permission.CONFIGURE_TEMPLATES)
