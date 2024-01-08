import os
from uuid import uuid1

from core.dataclasses.user_dataclass import ProfileDataClass


class PhotoService:
    @staticmethod
    def upload_avatar(instance: ProfileDataClass, file: str) -> str:
        ext = file.split('.')[-1]
        return os.path.join(instance.surname, 'avatar', f'{uuid1()}.{ext}')

    @staticmethod
    def upload_car_photo(instance, file: str) -> str:
        ext = file.split('.')[-1]
        return os.path.join('cars', f'{uuid1()}.{ext}')
