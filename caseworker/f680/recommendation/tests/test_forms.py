import pytest

from caseworker.f680.recommendation.constants import RecommendationType
from caseworker.f680.recommendation.forms.forms import BaseRecommendationForm, EntityConditionsRecommendationForm


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {},
            False,
            {
                "recommendation": ["Select if you approve or refuse"],
                "security_grading": ["Select the security classification"],
            },
        ),
        (
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "",
            },
            False,
            {"security_grading": ["Select the security classification"]},
        ),
        (
            {
                "recommendation": RecommendationType.APPROVE,
                # it is not possible to select this but if we were to submit then it fails as expected
                "security_grading": "confidential",
            },
            False,
            {"security_grading": ["Select a valid choice. confidential is not one of the available choices."]},
        ),
        (
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "official",
            },
            True,
            {},
        ),
        (
            {
                "recommendation": RecommendationType.REFUSE,
                "security_grading": "official",
            },
            True,
            {},
        ),
    ),
)
def test_make_recommendation_form_valid(data, valid_status, errors):
    release_request = {"id": "123465e5-4c80-4d0a-aef5-db94908b0417", "recipient": {"name": "Test entity"}}
    form = EntityConditionsRecommendationForm(data=data, release_request=release_request, proviso={"results": []})
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {},
            False,
            {
                "recommendation": ["Select if you approve or refuse"],
                "security_grading": ["Select the security classification"],
            },
        ),
        (
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "",
            },
            False,
            {"security_grading": ["Select the security classification"]},
        ),
        (
            {
                "recommendation": RecommendationType.APPROVE,
                # it is not possible to select this but if we were to submit then it fails as expected
                "security_grading": "confidential",
            },
            False,
            {"security_grading": ["Select a valid choice. confidential is not one of the available choices."]},
        ),
        (
            {
                "recommendation": RecommendationType.APPROVE,
                "security_grading": "official",
            },
            True,
            {},
        ),
        (
            {
                "recommendation": RecommendationType.REFUSE,
                "security_grading": "official",
            },
            True,
            {},
        ),
    ),
)
def test_make_recommendation_form_valid_no_provisos(data, valid_status, errors):
    release_request = {"id": "123465e5-4c80-4d0a-aef5-db94908b0417", "recipient": {"name": "Test entity"}}
    form = BaseRecommendationForm(data=data, release_request=release_request)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors
