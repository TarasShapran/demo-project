from django.urls import path

from apps.cars.views import AddPhotoByCarIdView, CarListCreateView, CarRetrieveUpdateDestroyView

urlpatterns = [
    path('', CarListCreateView.as_view()),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view()),
    path('/<int:pk>/photo', AddPhotoByCarIdView.as_view(), name='cars_add_photo')
]
