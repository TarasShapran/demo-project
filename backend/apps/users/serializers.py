from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import UserModel as User

from core.enums.regex_enum import RegEx
from core.services.email_service import EmailService

from django.contrib.auth import get_user_model
from django.core import validators as V
from django.db.transaction import atomic

from rest_framework import serializers

from apps.users.models import ProfileModel
from core.services.jwt_service import JWTService, RecoveryToken

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'avatar', 'created_at', 'updated_at')


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('avatar',)
        extra_kwargs = {
            'avatar': {
                'required': True
            }
        }


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(max_length=100, min_length=8, write_only=True, validators=[
        V.RegexValidator(*RegEx.PASSWORD.value)
    ])
    password2 = serializers.CharField(max_length=100, min_length=8, write_only=True, validators=[
        V.RegexValidator(*RegEx.PASSWORD.value)
    ])

    class Meta:
        model = UserModel
        fields = (
            'id', 'email', 'password', 'password2', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'created_at',
            'updated_at', 'profile'
        )
        read_only_fields = ('id', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'password2': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        profile = ProfileModel.objects.create(**profile)
        user = UserModel.objects.create_user(profile=profile, **validated_data)
        EmailService.register_email(user)
        return user


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('Token expired')
