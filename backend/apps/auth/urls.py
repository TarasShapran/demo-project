from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from .views import ActivateUserView, MeView, RecoveryPasswordRequestView, RecoveryPasswordView, SocketView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='auth_login'),
    path('/refresh', TokenRefreshView.as_view(), name='auth_refresh'),
    path('/me', MeView.as_view(), name='auth_me'),
    path('/activate/<str:token>', ActivateUserView.as_view(), name='auth_activate_user'),
    path('/recovery/request', RecoveryPasswordRequestView.as_view(), name='auth_recovery_password_request'),
    path('/recovery/<str:token>', RecoveryPasswordView.as_view(), name='auth_recovery_password'),
    path('/socket', SocketView.as_view(), name='auth_socket_tokenasa')
]
