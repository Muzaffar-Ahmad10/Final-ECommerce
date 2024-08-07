from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIA_FILES_LOCATION

    def url(self, name):
        url = super().url(name)
        return url.split('?')[0]
