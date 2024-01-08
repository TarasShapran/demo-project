from core.services.email_service import EmailService

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class TestEmailView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        EmailService.test_email()
        return Response('ok')
