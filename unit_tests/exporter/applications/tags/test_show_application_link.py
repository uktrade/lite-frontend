import pytest

from exporter.applications.templatetags.show_application_link import show_application_link


@pytest.mark.parametrize(
    "application, expected_link_output",
    [
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000004", "key": "submitted", "value": "Submitted"},
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Application 1",
                "case_type": {"reference": {"key": "siel"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000001/">Application 1</a>',
        ),
        (
            {
                "status": {
                    "id": "00000000-0000-0000-0000-000000000003",
                    "key": "initial_checks",
                    "value": "Initial checks",
                },
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Application 2",
                "case_type": {"reference": {"key": "siel"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000002/">Application 2</a>',
        ),
        (
            {
                "status": {
                    "id": "00000000-0000-0000-0000-000000000002",
                    "key": "under_review",
                    "value": "Under review",
                },
                "id": "00000000-0000-0000-0000-000000000003",
                "name": "Application 3",
                "case_type": {"reference": {"key": "siel"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000003/">Application 3</a>',
        ),
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000001", "key": "ogd_advice", "value": "OGD Advice"},
                "id": "00000000-0000-0000-0000-000000000004",
                "name": "Application 4",
                "case_type": {"reference": {"key": "siel"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000004/">Application 4</a>',
        ),
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
                "id": "00000000-0000-0000-0000-000000000005",
                "name": "Application 5",
                "case_type": {"reference": {"key": "siel"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000005/task-list/">Application 5</a>',
        ),
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
                "id": "00000000-0000-0000-0000-000000000006",
                "name": "Application 6",
                "case_type": {"reference": {"key": "f680"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/f680/00000000-0000-0000-0000-000000000006/apply/">Application 6</a>',
        ),
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000004", "key": "submitted", "value": "Submitted"},
                "id": "00000000-0000-0000-0000-000000000007",
                "name": "Application 7",
                "case_type": {"reference": {"key": "f680"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/f680/00000000-0000-0000-0000-000000000007/summary/">Application 7</a>',
        ),
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000004", "key": "submitted", "value": "Submitted"},
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Application 8",
                "case_type": {"reference": {"key": "export_licence"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000001/">Application 1</a>',
        ),
        (
            {
                "status": {
                    "id": "00000000-0000-0000-0000-000000000003",
                    "key": "initial_checks",
                    "value": "Initial checks",
                },
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Application 9",
                "case_type": {"reference": {"key": "export_licence"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000002/">Application 2</a>',
        ),
        (
            {
                "status": {
                    "id": "00000000-0000-0000-0000-000000000002",
                    "key": "under_review",
                    "value": "Under review",
                },
                "id": "00000000-0000-0000-0000-000000000003",
                "name": "Application 10",
                "case_type": {"reference": {"key": "export_licence"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000003/">Application 3</a>',
        ),
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000001", "key": "ogd_advice", "value": "OGD Advice"},
                "id": "00000000-0000-0000-0000-000000000004",
                "name": "Application 11",
                "case_type": {"reference": {"key": "export_licence"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000004/">Application 4</a>',
        ),
        (
            {
                "status": {"id": "00000000-0000-0000-0000-000000000000", "key": "draft", "value": "Draft"},
                "id": "00000000-0000-0000-0000-000000000005",
                "name": "Application 12",
                "case_type": {"reference": {"key": "export_licence"}},
            },
            '<a class="govuk-link govuk-link--no-visited-state app-icon-label" href="/applications/00000000-0000-0000-0000-000000000005/task-list/">Application 5</a>',
        ),
    ],
)
def test_show_application_link(application, expected_link_output):
    assert show_application_link(application) == expected_link_output
