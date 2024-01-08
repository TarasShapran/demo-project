from core.dataclasses.user_dataclass import ProfileDataClass, UserDataClass
from core.permissions import IsAdminOrWriteOnly, IsSuperUser

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.serializers import ProfileAvatarSerializer, UserSerializer

UserModel = get_user_model()


class UserCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrWriteOnly,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)


class UserAddAvatarView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileAvatarSerializer
    http_method_names = ('put',)

    def get_object(self):
        return UserModel.objects.get(pk=self.request.user.pk).profile

    def perform_update(self, serializer):
        profile: ProfileDataClass = self.get_object()
        profile.avatar.delete()
        super().perform_update(serializer)


class AdminToUserView(GenericAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: UserDataClass = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToAdminView(GenericAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: UserDataClass = self.get_object()
        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserBlockView(GenericAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: UserDataClass = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserUnBlockView(GenericAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: UserDataClass = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
