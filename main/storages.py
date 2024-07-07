from storages.backends.s3boto3 import S3Boto3Storage

class WasabiStorage(S3Boto3Storage):
    bucket_name = 'swsc'
    custom_domain = f'{bucket_name}.s3.wasabisys.com'