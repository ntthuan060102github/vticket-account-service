from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from vticket_app.helpers.session_provider import SessionProvider

class CustomJWTAuthentication(BaseAuthentication):
    session_provider = SessionProvider()

    def authenticate(self, request):
        bearer_token = request.headers.get("Authorization", None)

        if bearer_token is None:
            raise AuthenticationFailed("Missing token!")
        
        token = bearer_token.replace("Bearer ", "")

        if not self.session_provider.verify_token(token=token):
            raise AuthenticationFailed("Verify token failed!")