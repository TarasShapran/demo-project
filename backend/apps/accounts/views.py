from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()
        response.data['access_token'] = response.data.pop('access')
        response.data['refresh_token'] = response.data.pop('refresh')
        return response
