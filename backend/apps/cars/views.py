from core.permissions import IsAdminWriteOrIsAuthenticatedRead, IsSuperUser
from drf_yasg.utils import swagger_auto_schema

from django.utils.decorators import method_decorator

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import MultiPartRenderer
from rest_framework.request import Request

from apps.cars.filters import CarFilter
from apps.cars.models import CarModel
from apps.cars.serializers import CarPhotoSerializer, CarSerializer


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


class AddPhotoByCarIdView(UpdateAPIView):
    permission_classes = (IsAdminWriteOrIsAuthenticatedRead,)
    serializer_class = CarPhotoSerializer
    queryset = CarModel.objects.all()
    http_method_names = ('put',)
    parser_classes = MultiPartRenderer,

    def perform_update(self, serializer):
        car = self.get_object()
        car.photo.delete()
        super().perform_update(serializer)
