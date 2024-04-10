from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from vticket_app.models.user import User
from vticket_app.services.authentication_service import AuthenticationService

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    authentication_service = AuthenticationService()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        _validated_data = super().validate(attrs)

        refresh_payload = self.token_class(_validated_data["refresh"]).payload
        refresh_jti = refresh_payload["jti"]

        access_jti = self.token_class.access_token_class(_validated_data["access"]).payload["jti"]

        user_id = refresh_payload["user_id"]
        user = User.objects.get(id=user_id)
        self.authentication_service.save_session(user, access_jti, refresh_jti)
        
        return _validated_data