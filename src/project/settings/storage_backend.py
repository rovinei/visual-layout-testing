from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = settings.AWS_MEDIA_LOCATION
    file_overwrite = True


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    file_overwrite = True


class ReportStorage(S3Boto3Storage):
    location = settings.AWS_GALEN_REPORT_LOCATION
    file_overwrite = True


class SpecFileStorage(S3Boto3Storage):
    location = settings.SPEC_FILE_LOCATION
    file_overwrite = True
    default_acl = 'public-read'