import os
import uuid
import boto3
from datetime import datetime
from django.utils import timezone

from conf.settings import env


def upload_test_document_to_aws():
    bucket_name = env('AWS_STORAGE_BUCKET_NAME')
    s3 = boto3.client('s3', aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'))
    # s3_key = datetime.strftime(timezone.now(), '%Y-%m-%d-%H-%M-%S--') + str(uuid.uuid4()) + '--lite-test-doc.jpg'
    s3_key = 'lite-test-doc.jpg'

    file_to_upload_abs_path = \
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_files', 'cat.jpg'))

    s3.upload_file(file_to_upload_abs_path, bucket_name, s3_key)
    return s3_key
