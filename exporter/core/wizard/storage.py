from storages.backends.s3boto3 import S3Boto3Storage


class NoSaveStorage(S3Boto3Storage):
    def save(self, name, content, max_length=None):
        # We don't actually need to save anything here as our file is already
        # on S3.
        return content.obj.key

    def delete(self, name):
        # We don't actually want to delete anything here as we'll be sending
        # the key to the API that will pick this up so we want it to persist
        # in the S3 bucket.
        pass
