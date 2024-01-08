from django.urls import path

from .views import AdminToUserView, UserAddAvatarView, UserBlockView, UserCreateView, UserToAdminView, UserUnBlockView

urlpatterns = [
    path('', UserCreateView.as_view(), name='users_create'),
    path('/avatars', UserAddAvatarView.as_view(), name='users_add_avatar'),
    path('/<int:pk>/to_admin', UserToAdminView.as_view(), name='users_to_admin'),
    path('/<int:pk>/to_user', AdminToUserView.as_view(), name='users_to_user'),
    path('/<int:pk>/block', UserBlockView.as_view(), name='users_block'),
    path('/<int:pk>/un_block', UserUnBlockView.as_view(), name='users_un_block'),
]
