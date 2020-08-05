from django.urls import reverse

from lite_content.lite_internal_frontend.cases import ComplianceForms
from lite_forms.components import Form, BackLink, DateInput, Select, Option, TextArea, Custom

Visit_type_choices = [
    Option("first_contact", "First contact"),
    Option("first_visit", "First visit"),
    Option("routine_visit", "Routine visit"),
    Option("revisit", "Revisit"),
]

risk_value = [
    Option("very_low", "Very low risk"),
    Option("lower", "Lower risk"),
    Option("medium", "Medium risk"),
    Option("higher", "Higher risk"),
    Option("highest", "Highest risk"),
]

licence_risk_value = [
    Option(str(1), str(1)),
    Option(str(2), str(2)),
    Option(str(3), str(3)),
    Option(str(4), str(4)),
    Option(str(5), str(5)),
]


def visit_report_form(queue_pk, pk):
    return Form(
        title=ComplianceForms.VisitReport.TITLE,
        questions=[
            Select(title=ComplianceForms.VisitReport.VISIT_TYPE, name="visit_type", options=Visit_type_choices),
            DateInput(
                title=ComplianceForms.VisitReport.VISIT_DATE,
                description=ComplianceForms.VisitReport.VISIT_DATE_DESCRIPTION,
                name="visit_date",
                prefix="visit_date_",
            ),
            Select(title=ComplianceForms.VisitReport.OVERALL_RISK_VALUE, name="overall_risk_value", options=risk_value),
            Select(
                title=ComplianceForms.VisitReport.LICENCE_RISK_VALUE,
                name="licence_risk_value",
                options=licence_risk_value,
            ),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def people_present_form(queue_pk, pk):
    return Form(
        title=ComplianceForms.PeoplePresent.TITLE,
        description=ComplianceForms.PeoplePresent.DESCRIPTION,
        questions=[Custom(template="components/people-present.html")],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
        container="case",
    )


def overview_form(queue_pk, pk):
    return Form(
        title=ComplianceForms.Overview.TITLE,
        questions=[TextArea(name="overview", extras={"max_length": 750})],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def inspection_form(queue_pk, pk):
    return Form(
        title=ComplianceForms.Inspection.TITLE,
        questions=[TextArea(name="inspection", extras={"max_length": 750})],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def compliance_with_licence_form(queue_pk, pk):
    return Form(
        title=ComplianceForms.ComplianceWithLicence.TITLE,
        description=ComplianceForms.ComplianceWithLicence.DESCRIPTION,
        questions=[
            TextArea(
                title=ComplianceForms.ComplianceWithLicence.OVERVIEW,
                name="compliance_overview",
                extras={"max_length": 750},
            ),
            Select(
                title=ComplianceForms.ComplianceWithLicence.RISK_VALUE, name="compliance_risk_value", options=risk_value
            ),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def knowledge_of_people_form(queue_pk, pk):
    return Form(
        title=ComplianceForms.KnowledgeOfPeople.TITLE,
        questions=[
            TextArea(
                title=ComplianceForms.KnowledgeOfPeople.OVERVIEW,
                name="individuals_overview",
                extras={"max_length": 750},
            ),
            Select(
                title=ComplianceForms.KnowledgeOfPeople.RISK_VALUE, name="individuals_risk_value", options=risk_value
            ),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def knowledge_of_products_form(queue_pk, pk):
    return Form(
        title=ComplianceForms.KnowledgeOfProducts.TITLE,
        questions=[
            TextArea(
                title=ComplianceForms.KnowledgeOfProducts.OVERVIEW, name="products_overview", extras={"max_length": 750}
            ),
            Select(
                title=ComplianceForms.KnowledgeOfProducts.RISK_VALUE, name="products_risk_value", options=risk_value
            ),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )
