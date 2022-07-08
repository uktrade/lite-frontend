import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def good(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]


@pytest.fixture
def good_detail_summary_check_your_answers_url(application):
    return reverse(
        "applications:good_detail_summary",
        kwargs={
            "pk": application["id"],
        },
    )


def test_good_detail_summary_check_your_answers_view_status_code(
    authorized_client,
    requests_mock,
    mock_application_get,
    good_detail_summary_check_your_answers_url,
    application,
    good,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    assert response.status_code == 200


def test_good_detail_summary_check_your_answers_view_template_used(
    authorized_client,
    requests_mock,
    mock_application_get,
    good_detail_summary_check_your_answers_url,
    application,
    good,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    assertTemplateUsed(response, "applications/goods/goods-detail-summary.html")


def test_good_detail_summary_check_your_answers_context(
    authorized_client,
    requests_mock,
    mock_application_get,
    good_detail_summary_check_your_answers_url,
    application,
    good,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    context = response.context

    assert context["application_id"] == application["id"]
    assert [good for good, _ in context["goods"]] == application["goods"]
    assert [summary for _, summary in context["goods"]] == [
        (
            ("firearm-type", "Firearms", "Select the type of firearm product"),
            ("firearm-category", "Non automatic shotgun, Non automatic rim-fired handgun", "Firearm category"),
            ("name", "p1", "Give the product a descriptive name"),
            (
                "is-good-controlled",
                "Yes",
                "Do you know the product's control list entry?",
            ),
            ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
            (
                "is-pv-graded",
                "Yes",
                "Does the product have a government security grading or classification?",
            ),
            ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
            (
                "pv-grading-grading",
                "Official",
                "What is the security grading or classification?",
            ),
            ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
            (
                "pv-grading-issuing-authority",
                "Government entity",
                "Name and address of the issuing authority",
            ),
            ("pv-grading-details-reference", "GR123", "Reference"),
            ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
            ("calibre", "0.25", "What is the calibre of the product?"),
            ("is-replica", "No", "Is the product a replica firearm?"),
            (
                "is-registered-firearms-dealer",
                "No",
                "Are you a registered firearms dealer?",
            ),
            (
                "is-covered-by-firearm-act-section-one-two-or-five-explanation",
                "Not covered by firearm act sections",
                "Explain",
            ),
            (
                "has-product-document",
                "Yes",
                "Do you have a document that shows what your product is and what it’s designed to do?",
            ),
            (
                "is-document-sensitive",
                "No",
                "Is the document rated above Official-sensitive?",
            ),
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" href="/goods/8b730c06-ab4e-401c-aeb0-32b3c92e912c/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
            (
                "product-document-description",
                "product data sheet",
                "Description (optional)",
            ),
            ("manufacture-year", "1990", "What year was it made?"),
            (
                "is-onward-exported",
                "No",
                "Will the product be onward exported to any additional countries?",
            ),
            ("is-deactivated", "No", "Has the product been deactivated?"),
            ("number-of-items", 2, "Number of items"),
            ("total-value", "£444.00", "Total value"),
            (
                "has-serial-numbers",
                "Yes, I can add serial numbers now",
                "Will each product have a serial number or other identification marking?",
            ),
            (
                "serial-numbers",
                "\n"
                "\n"
                "\n"
                '    <details class="govuk-details govuk-!-margin-bottom-0" '
                'data-module="govuk-details">\n'
                '        <summary class="govuk-details__summary">\n'
                '            <span class="govuk-details__summary-text">\n'
                "                View serial numbers\n"
                "            </span>\n"
                "        </summary>\n"
                '        <div class="govuk-details__text">\n'
                "            \n"
                "                1. 12345<br>\n"
                "            \n"
                "                2. ABC-123\n"
                "            \n"
                "        </div>\n"
                "    </details>\n"
                "\n",
                "Enter serial numbers or other identification markings",
            ),
        ),
        None,
    ]
    assert not context["is_user_rfd"]
    assert not context["application_status_draft"]
    assert context["organisation_documents"] == {}
    assert not context["feature_flag_product_2_0"]


def test_good_detail_summary_check_your_answers_non_firearm_product_type(
    authorized_client,
    requests_mock,
    mock_application_get,
    good_detail_summary_check_your_answers_url,
    application,
    good,
):
    requests_mock.get(
        f"/applications/{application['id']}/goods/{good['good']['id']}/documents/",
        json={"documents": []},
    )
    application["goods"][0]["firearm_details"] = None

    response = authorized_client.get(good_detail_summary_check_your_answers_url)
    context = response.context

    assert context["application_id"] == application["id"]
    assert [good for good, _ in context["goods"]] == application["goods"]
    assert [summary for _, summary in context["goods"]] == [None, None]
    assert not context["is_user_rfd"]
    assert not context["application_status_draft"]
    assert context["organisation_documents"] == {}
    assert not context["feature_flag_product_2_0"]
