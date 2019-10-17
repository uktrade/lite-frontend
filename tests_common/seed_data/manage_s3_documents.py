import os
import boto3

from conf.settings import env


def upload_test_document_to_aws():
    bucket_name = env('AWS_STORAGE_BUCKET_NAME')
    s3 = boto3.client('s3', aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'))
    # Use a fully static S3 key so that only one file will ever exist in the S3 bucket and
    # we don't end up filling the bucket with lots of files that don't get deleted
    s3_key = 'lite-test-doc.jpg'

    file_to_upload_abs_path = \
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_files', 'cat.jpg'))

    s3.upload_file(file_to_upload_abs_path, bucket_name, s3_key)
    return s3_key
