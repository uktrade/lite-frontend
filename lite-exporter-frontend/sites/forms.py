from lite_content.lite_exporter_frontend import strings
from django.urls import reverse_lazy

from lite_forms.common import address_questions
from lite_forms.components import Heading, BackLink, Form, TextInput
from lite_forms.styles import HeadingStyle

from core.services import get_countries


def new_site_form():
    return Form(
        title=strings.Sites.CREATE,
        description="",
        questions=[
            TextInput(title="Name of site", name="name"),
            Heading("Where is the site based?", HeadingStyle.M),
            *address_questions(get_countries(None, True)),
        ],
        back_link=BackLink("Back to Sites", reverse_lazy("sites:sites")),
    )


def edit_site_form(site):
    return Form(
        title=strings.sites.SitesPage.EDIT + site["name"],
        questions=[
            TextInput(title="Name of site", name="name"),
            Heading("Where is the site based?", HeadingStyle.M),
            *address_questions(get_countries(None, True)),
        ],
        back_link=BackLink(
            strings.sites.SitesPage.BACK_TO + site["name"], reverse_lazy("sites:site", kwargs={"pk": site["id"]})
        ),
    )
