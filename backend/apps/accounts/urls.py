from django.urls import path, include

from apps.accounts.views import GoogleLogin

urlpatterns = [
    path("/google/", GoogleLogin.as_view(), name="google_login"),

]
