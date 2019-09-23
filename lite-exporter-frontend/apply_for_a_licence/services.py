from conf.settings import AWS_STORAGE_BUCKET_NAME, STREAMING_CHUNK_SIZE
from django.http import StreamingHttpResponse
from s3chunkuploader.file_handler import s3_client


def add_document_data(request):
    files = request.FILES.getlist("file")
    if not files:
        return None, 'No files attached'
    if len(files) != 1:
        return None, 'Multiple files attached'

    file = files[0]
    try:
        original_name = file.original_name
    except Exception: # noqa
        original_name = file.name

    data = {
        'name': original_name,
        's3_key': file.name,
        'size': int(file.size // 1024) if file.size else 0,  # in kilobytes
    }
    if 'description' in request.POST:
        data['description'] = request.POST.get('description')

    return data, None


# Stream file
def generate_file(result):
    for chunk in iter(lambda: result['Body'].read(STREAMING_CHUNK_SIZE), b''):
        yield chunk


def download_document_from_s3(s3_key, original_file_name):
    s3 = s3_client()
    s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    _kwargs = {}
    if s3_response.get('ContentType'):
        _kwargs['content_type'] = s3_response['ContentType']
    response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
    response['Content-Disposition'] = f'attachment; filename="{original_file_name}"'
    return response
