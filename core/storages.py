from storages.backends.s3boto3 import S3Boto3Storage


class MinioBaseStorage(S3Boto3Storage):
    """
    Shared S3-compatible storage settings for MinIO.
    Bucket policy should control public access where needed.
    """

    default_acl = None
    querystring_auth = False


class MediaStorage(MinioBaseStorage):
    location = "media"
    file_overwrite = False


class StaticStorage(MinioBaseStorage):
    location = "static"
    file_overwrite = True
