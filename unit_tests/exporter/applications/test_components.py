from exporter.applications.components import footer_label


def test_footer_label(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    lbl = footer_label(application_id)

    assert (
        'Or <a class="govuk-link govuk-link--no-visited-state"'
        f' rel="noreferrer noopener" target="_blank" href="/applications/{application_id}/task-list/">'
        "return to application overview</a>"
    ) == lbl.text
