from django.conf import settings


from core import client


def post_exporter_answer_set(request, flow, section, target_content_type, target_object_id, answers, questions):
    data = {
        "flow": flow,
        "section": section,
        "answers": answers,
        "questions": questions,
        "frontend_commit_sha": settings.GIT_COMMIT,
        "target_content_type": target_content_type,
        "target_object_id": target_object_id,
    }
    response = client.post(request, f"/exporter/exporter-answers/exporter-answer-set/", data)
    return response.json(), response.status_code


def get_exporter_answer_set(request, target_object_id):
    response = client.get(
        request, f"/exporter/exporter-answers/exporter-answer-set/?target_object_id={target_object_id}&status=draft"
    )
    return response.json(), response.status_code
