import logging

from core.permissions import IsAdminWriteOrIsAuthenticatedRead, IsSuperUser
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Avg, F
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cars.filters import CarFilter
from apps.cars.models import CarCurrencyPriceModel, CarDetailsModel, CarModel
from apps.cars.serializers import CarCurrencyPriceSerializer, CarDetailsSerializer, CarPhotoSerializer, CarSerializer

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
    # permission_classes = (IsAdminWriteOrIsAuthenticatedRead,)
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        car = self.get_object()
        serializer = self.get_serializer(car)
        user = request.user
        if user:
            queryset = CarDetailsModel.objects.filter(car=car, user_viewed=user)
            if not queryset.exists():
                    data = {'car': car.id, 'user_viewed': user.id, 'views': 1}
                    car_details_serializer = CarDetailsSerializer(data=data)
                    car_details_serializer.is_valid(raise_exception=True)
                    car_details_serializer.save()
            else:
                car_details_serializer = CarDetailsSerializer(car=car, user_viewed=user.id)
                car_details_serializer.is_valid(raise_exception=True)
                car_details_serializer.save()

        logger.info(f"request: {request}")
        x_forwarded_for = request.META
        x_host = request.META.get('REMOTE_HOST')

        logger.info(f'META:  {x_forwarded_for}')
        logger.info(f'IP HOST {x_host}')
        # type(instance).objects.filter(pk=instance.pk).update(
        #     views=F('views') + 1,
        # )

        return Response(serializer.data)


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
    queryset = CarCurrencyPriceModel.objects.all()
    serializer_class = CarCurrencyPriceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (super()
                .get_queryset()
                .filter(currency='USD'))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CarCurrencyPriceSerializer(queryset, many=True)
        logger.info(serializer.data)

        avg_price = queryset.aggregate(avg_price=Avg('amount'))
        logger.info(f'avg_price: {avg_price}')
        avg_price = avg_price['avg_price']
        logger.info(avg_price)
        return Response(avg_price, status.HTTP_200_OK)
