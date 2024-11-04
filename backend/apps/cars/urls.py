from django.urls import path

from apps.cars.views import (
    AddPhotoByCarIdView,
    CarListCreateView,
    CarRetrieveUpdateDestroyView,
    GetAveragePriceByRegionView,
)

urlpatterns = [
    path('', CarListCreateView.as_view()),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view()),
    path('/<int:pk>/photo', AddPhotoByCarIdView.as_view(), name='cars_add_photo'),
    path('/average_price', GetAveragePriceByRegionView.as_view(), name='cars_get_average_price'),
]
