from exporter.core.constants import ProductSecurityFeatures


def test_product_security_features():
    TITLE = "Does the product include security features to protect information?"
    SECURITY_FEATURE_DETAILS = "Provide details of the information security features"
    SUBTITLE = "For example, authentication, encryption or any other information security controls."
    HELP_TEXT = """Information security features include cryptography, authentication, and cryptanalytic functions.
    They are often found in communication, wireless or internet-based products."""

    assert TITLE == ProductSecurityFeatures.TITLE
    assert SECURITY_FEATURE_DETAILS == ProductSecurityFeatures.SECURITY_FEATURE_DETAILS
    assert SUBTITLE == ProductSecurityFeatures.SUBTITLE
    assert HELP_TEXT == ProductSecurityFeatures.HELP_TEXT
