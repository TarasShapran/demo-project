from django.urls import path

from .views import TestEmailView

urlpatterns = {
    path('', TestEmailView.as_view())
}
