import json
from django.core.cache import cache
from rest_framework_simplejwt.settings import api_settings as jwt_configs

from vticket_app.models.user import User
from vticket_app.serializers.user_serializer import UserSerializer

class AuthenticationService():
    account_serializer = UserSerializer

    def save_session(self, user: User):
        _session_data = self.account_serializer(user, many=False, exclude=["password"]).data
        cache.set(f"session:{user.id}:access", json.dumps(_session_data), jwt_configs.ACCESS_TOKEN_LIFETIME.seconds)
        cache.set(f"session:{user.id}:refresh", user.id, jwt_configs.ACCESS_TOKEN_LIFETIME.seconds)