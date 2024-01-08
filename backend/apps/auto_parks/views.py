from core.permissions import IsAdminWriteOrIsAuthenticatedRead

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.auto_parks.models import AutoParkModel
from apps.auto_parks.serializers import AutoParkSerializer
from apps.cars.serializers import CarSerializer


class AutoParkListCreateView(ListCreateAPIView):
    queryset = AutoParkModel.objects.all()
    serializer_class = AutoParkSerializer
    permission_classes = (IsAdminWriteOrIsAuthenticatedRead,)


class AutoParkAddCarView(GenericAPIView):
    queryset = AutoParkModel.objects.all()
    permission_classes = (IsAdminWriteOrIsAuthenticatedRead,)

    def post(self, *args, **kwargs):
        auto_park = self.get_object()
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(auto_park=auto_park)
        park_serializer = AutoParkSerializer(auto_park)
        return Response(park_serializer.data, status.HTTP_201_CREATED)
