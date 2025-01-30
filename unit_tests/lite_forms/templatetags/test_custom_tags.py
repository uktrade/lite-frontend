import pytest

from pytest_django.asserts import assertHTMLEqual

from lite_forms.templatetags import custom_tags


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test.pdf", "pdf"),
        ("test", "file"),
    ],
)
def test_file_type(filename, expected):
    assert expected == custom_tags.file_type(filename)


@pytest.mark.parametrize(
    "input, context, expected",
    [
        (
            "{% govuk_link_button text='tests.TestPage.BUTTON' url='core:index' %}",
            {},
            '<a href="/" role="button" draggable="false" class="govuk-button" data-module="govuk-button">Test Button</a>',
        ),
        (
            "{% govuk_link_button text='tests.TestPage.BUTTON' url='core:index' id='test-id' classes='govuk-button--secondary' %}",
            {},
            '<a id="button-test-id" href="/" role="button" draggable="false" class="govuk-button govuk-button--secondary" data-module="govuk-button">Test Button</a>',
        ),
        (
            "{% govuk_link_button text='tests.TestPage.BUTTON' url='core:index' show_chevron=True %}",
            {},
            '<a href="/" role="button" draggable="false" class="govuk-button" data-module="govuk-button">Test Button<svg aria-hidden="true" class="govuk-button__start-icon" focusable="false" height="15" viewbox="0 0 33 43" width="13" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h13l20 20-20 20H0l20-20z" fill="currentColor"></svg></a>',
        ),
        (
            "{% govuk_link_button text='tests.TestPage.BUTTON' url='core:index' query_params='?foo=bar' %}",
            {},
            '<a href="/?foo=bar" role="button" draggable="false" class="govuk-button" data-module="govuk-button">Test Button</a>',
        ),
        (
            "{% govuk_link_button text='tests.TestPage.BUTTON' url='core:index' hidden=True %}",
            {},
            '<a href="/" role="button" draggable="false" class="govuk-button" data-module="govuk-button" style="display: none;">Test Button</a>',
        ),
        (
            "{% govuk_link_button text='tests.TestPage.BUTTON' url='core:index' query_params=html_content %}",
            {"html_content": '">foo</a><script>alert("xss")</script><a href="blah'},
            '<a href="/&quot;&gt;foo&lt;/a&gt;&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;&lt;a href=&quot;blah" role="button" draggable="false" class="govuk-button " data-module="govuk-button">Test Button</a>',
        ),
    ],
)
def test_govuk_link_button(render_template_string, input, context, expected):
    assertHTMLEqual(render_template_string(input, context), expected)
