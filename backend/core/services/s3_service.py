from core.services.photo_service import PhotoService
from storages.backends.s3boto3 import S3Boto3Storage

AVATAR_LOCATION = 'car_images'
AVATAR_STORAGE = 'UploadFiles.storage_backends.CarImages'


class CarStorage(S3Boto3Storage):
    location = AVATAR_LOCATION
    default_acl = 'public-read'
    file_overwrite = False

    def _normalize_name(self, name):
        name = PhotoService.upload_car_photo(file=name)
        return super()._normalize_name(name)
