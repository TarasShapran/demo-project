import logging

from core.permissions import IsAdminWriteOrIsAuthenticatedRead, IsSuperUser
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Avg
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cars.filters import CarFilter
from apps.cars.models import CarModel
from apps.cars.serializers import CarPhotoSerializer, CarSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class CarListCreateView(ListAPIView):
    """
    Get all cars
    """
    queryset = CarModel.my_objects.all()
    serializer_class = CarSerializer
    filterset_class = CarFilter
    # permission_classes = (IsAdminWriteOrIsAuthenticatedRead,)
    permission_classes = (AllowAny,)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Get Car by ID
    put:
        Update Car by ID
    patch:
        Update Car by ID
    delete:
        Delete Car by ID
    """
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminWriteOrIsAuthenticatedRead,)


class AddPhotoByCarIdView(GenericAPIView):
    queryset = CarModel.objects.all()
    permission_classes = (IsAdminWriteOrIsAuthenticatedRead,)

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        images = request.data.getlist('image', [])
        for image in images:
            data = {'image': image}
            photo_serializer = CarPhotoSerializer(data=data)
            photo_serializer.is_valid(raise_exception=True)
            photo_serializer.save(car=car)
        car_serializer = CarSerializer(car)
        return Response(car_serializer.data, status.HTTP_201_CREATED)


class GetAveragePriceByRegionView(ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return super().get_queryset().filter(region=self.request.data.pop('region'))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        avg_price = queryset.aggregate(avg_price=Avg('price'))
        logger.info(f'avg_price: {avg_price}')
        avg_price = avg_price['avg_price']
        logger.info(avg_price)
        return Response(avg_price, status.HTTP_200_OK)