from core import client


def get_exporter_answer_set(request, target_object_id):
    response = client.get(
        request, f"/caseworker/exporter-answers/exporter-answer-set/?target_object_id={target_object_id}&status=active"
    )
    return response.json(), response.status_code
