import pytest

from caseworker.f680.recommendation.constants import RecommendationType
from caseworker.f680.recommendation.forms.forms import (
    BasicRecommendationForm,
    EntityConditionsForm,
    EntityRefusalReasonsForm,
    EntitySelectionAndDecisionForm,
)


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {},
            False,
            {
                "release_requests": ["Select entities to add recommendations"],
                "recommendation": ["Select if you approve or refuse"],
            },
        ),
        (
            {
                "release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
            },
            False,
            {
                "recommendation": ["Select if you approve or refuse"],
            },
        ),
        (
            {
                "release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
                "recommendation": RecommendationType.APPROVE,
            },
            True,
            {},
        ),
        (
            {
                "release_requests": ["123465e5-4c80-4d0a-aef5-db94908b0417"],
                "recommendation": RecommendationType.REFUSE,
            },
            True,
            {},
        ),
    ),
)
def test_entity_selection_and_decision_form_valid(data, valid_status, errors):
    release_requests = [
        {
            "id": "123465e5-4c80-4d0a-aef5-db94908b0417",
            "recipient": {
                "name": "Test entity",
                "country": {
                    "name": "Australia",
                },
            },
        }
    ]
    form = EntitySelectionAndDecisionForm(data=data, release_requests=release_requests)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {
                "conditions": [],
            },
            False,
            {
                "security_grading": ["Select the security classification"],
            },
        ),
        (
            {
                "security_grading": "official",
                "conditions": ["no_release"],
            },
            True,
            {},
        ),
    ),
)
def test_entity_conditions_form_valid(data, valid_status, errors):
    conditions = [{"name": "no_release", "text": "No release"}]
    form = EntityConditionsForm(data=data, conditions={"results": conditions})
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid_status, errors",
    (
        (
            {},
            False,
            {"refusal_reasons": ["Enter refusal reasons"]},
        ),
        (
            {
                "refusal_reasons": ["1"],
            },
            True,
            {},
        ),
    ),
)
def test_entity_refusal_reasons_form_valid(data, valid_status, errors):
    denial_reasons = {"1": [("1", "1"), "1a", "1a"], "2": [("2a", "2a")]}
    reasons = [{"id": "1", "display_value": "1", "description": "does not meet criteria"}]
    form = EntityRefusalReasonsForm(data=data, denial_reasons_choices=denial_reasons.items(), refusal_reasons=reasons)
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
                "security_grading": ["Select the security classification"],
            },
        ),
        (
            {
                "security_grading": "official",
                "conditions": "No concerns",
            },
            True,
            {},
        ),
    ),
)
def test_make_recommendation_form_valid_no_provisos(data, valid_status, errors):
    form = BasicRecommendationForm(data=data)
    assert form.is_valid() == valid_status
    if not valid_status:
        assert form.errors == errors
