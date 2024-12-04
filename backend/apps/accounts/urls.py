from django.urls import path, include

from apps.accounts.views import GoogleLoginView

urlpatterns = [
    path("/google/", GoogleLoginView.as_view(), name="google_login"),
]
