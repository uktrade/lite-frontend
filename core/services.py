from core import client


def stream_document(request, pk):
    response = client.get(request, f"/documents/stream/{pk}/", stream=True)
    return response, response.status_code
