from unittest import mock

from django.http import HttpRequest

from caseworker.users.middleware import RequestUserMiddleware


@mock.patch("caseworker.users.middleware.get_gov_user")
def test_request_user_middleware_process_view_no_user_id_in_session(mock_get_gov_user):
    request = HttpRequest()
    request.session = {}
    RequestUserMiddleware(mock.Mock()).process_view(request, None, None, None)
    mock_get_gov_user.assert_not_called()
    assert not hasattr(request, "user")


@mock.patch("caseworker.users.middleware.get_gov_user")
def test_request_queue_middleware_process_view_api_error(mock_get_gov_user):
    mock_get_gov_user.return_value = ({}, 500)
    request = HttpRequest()
    request.session = {"lite_api_user_id": "some-user-id"}
    RequestUserMiddleware(mock.Mock()).process_view(request, None, None, None)
    mock_get_gov_user.assert_called_with(request, "some-user-id")
    assert not hasattr(request, "user")


@mock.patch("caseworker.users.middleware.get_gov_user")
def test_request_queue_middleware_process_view_success(mock_get_gov_user):
    mock_get_gov_user.return_value = ({"user": "some-user"}, 200)
    request = HttpRequest()
    request.session = {"lite_api_user_id": "some-user-id"}
    RequestUserMiddleware(mock.Mock()).process_view(request, None, None, None)
    mock_get_gov_user.assert_called_with(request, "some-user-id")
    assert request.user == "some-user"
