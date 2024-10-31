from unittest import mock

from django.http import HttpRequest

from caseworker.queues.middleware import RequestQueueMiddleware


@mock.patch("caseworker.queues.middleware.get_queue")
def test_request_queue_middleware_process_view_queue_pk_in_kwargs(mock_get_queue):
    mock_get_queue.return_value = {"id": "some_queue"}
    request = HttpRequest()
    request.session = {"lite_api_user_id": "fake-user-id"}
    RequestQueueMiddleware(mock.Mock()).process_view(request, None, None, {"queue_pk": "test-queue-id"})
    mock_get_queue.assert_called_with(request, "test-queue-id")
    assert request.queue == mock_get_queue.return_value


@mock.patch("caseworker.queues.middleware.get_queue")
def test_request_queue_middleware_process_view_queue_pk_missing(mock_get_queue):
    mock_get_queue.return_value = {"id": "some_queue"}
    request = HttpRequest()
    request.session = {"lite_api_user_id": "fake-user-id"}
    RequestQueueMiddleware(mock.Mock()).process_view(request, None, None, {})
    mock_get_queue.assert_not_called()
    assert not hasattr(request, "queue")


@mock.patch("caseworker.queues.middleware.get_queue")
def test_request_queue_middleware_process_view_queue_request_403s(mock_get_queue):
    mock_get_queue.return_value = {"id": "some_queue"}
    request = HttpRequest()
    request.session = {}
    RequestQueueMiddleware(mock.Mock()).process_view(request, None, None, {"queue_pk": "test-queue-id"})
    mock_get_queue.assert_not_called()
    assert not hasattr(request, "queue")
