from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from vticket_app.models.user import User
from vticket_app.services.authentication_service import AuthenticationService

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    authentication_service = AuthenticationService()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        _validated_data = super().validate(attrs)
        user_id = self.token_class(attrs["refresh"]).payload["user_id"]
        user = User.objects.get(id=user_id)
        self.authentication_service.save_session(user=user)
        return _validated_data