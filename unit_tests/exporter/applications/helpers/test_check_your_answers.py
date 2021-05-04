from exporter.applications.helpers import check_your_answers


def test_convert_goods_on_application_no_answers(data_good_on_application):

    # given the canonical good does not have is_good_controlled set
    data_good_on_application["is_good_controlled"] = None
    data_good_on_application["good"]["is_good_controlled"] = None
    data_good_on_application["good"]["control_list_entries"] = []
    actual = check_your_answers.convert_goods_on_application([data_good_on_application])

    # then the differences in export characteristics are highlighted
    assert len(actual) == 1
    assert actual[0]["Controlled"] == "N/A"
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'


def test_convert_goods_on_application_application_level_control_list_entries(data_good_on_application):
    data_good_on_application["good"]["control_list_entries"] = []

    # given the canonical good and good in application have different export control characteristics
    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application([data_good_on_application])

    # then the differences in export characteristics are highlighted
    assert len(actual) == 1
    assert actual[0]["Controlled"] == "<span class='strike'>No</span><br> Yes"
    assert actual[0]["Control list entries"] == (
        "<span class='strike'><span class=\"govuk-hint govuk-!-margin-0\">N/A</span></span> "
        "<span data-definition-title='ML1' data-definition-text='Smooth-bore weapons...'>ML1</span>, "
        "<span data-definition-title='ML2' data-definition-text='Smooth-bore weapons...'>ML2</span>"
    )


def test_convert_goods_on_application_application_level_control_list_entries_same(data_good_on_application):
    # given the canonical good and good in application have same export control characteristics
    data_good_on_application["good"]["is_good_controlled"] = data_good_on_application["is_good_controlled"]
    data_good_on_application["good"]["control_list_entries"] = data_good_on_application["control_list_entries"]

    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application([data_good_on_application])

    # then no difference is highlighted
    assert len(actual) == 1
    assert actual[0]["Controlled"] == "Yes"
    assert actual[0]["Control list entries"] == (
        "<span data-definition-title='ML1' data-definition-text='Smooth-bore weapons...'>ML1</span>, "
        "<span data-definition-title='ML2' data-definition-text='Smooth-bore weapons...'>ML2</span>"
    )


def test_convert_goods_on_application_good_level_control_list_entries(data_good_on_application):
    # given the good has not been reviewed at application levcle
    data_good_on_application["is_good_controlled"] = None
    data_good_on_application["good"]["control_list_entries"] = []

    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application([data_good_on_application])

    # then no difference is highlighted
    assert len(actual) == 1
    assert actual[0]["Controlled"] == "No"
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'
