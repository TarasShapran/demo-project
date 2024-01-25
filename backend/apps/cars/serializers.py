from rest_framework import serializers

from apps.cars.models import CarImagesModel, CarModel


class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImagesModel
        fields = ('image',)


class CarSerializer(serializers.ModelSerializer):
    car_images = CarPhotoSerializer(read_only=True, many=True)

    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'price', 'year', 'body', 'car_images', 'created_at', 'updated_at')


    # def validate_brand(self, brand):
    #     if brand == 'Sas':
    #         raise serializers.ValidationError({'detail': 'brand == Sas'})
    #     return brand
    #
    # def validate(self, attrs):
    #     price = attrs['price']
    #     year = attrs['year']
    #     if price == year:
    #         raise serializers.ValidationError({'detail': 'year==price'})
    #     return attrs
