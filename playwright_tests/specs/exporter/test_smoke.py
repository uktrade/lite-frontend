def test_smoke(page):
    page.goto("/")

    header = page.locator(".govuk-heading-xl")
    assert "Export control account: sign in or set up" in header.text_content()
