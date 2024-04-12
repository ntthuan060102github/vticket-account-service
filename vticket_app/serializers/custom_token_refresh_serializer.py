from typing import Any, Dict
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from vticket_app.models.user import User
from vticket_app.services.authentication_service import AuthenticationService
from vticket_app.helpers.session_provider import SessionProvider

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    authentication_service = AuthenticationService()
    session_provider = SessionProvider()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        _validated_data = super().validate(attrs)

        if not self.session_provider.verify_refresh_token(attrs["refresh"]):
            raise ValidationError("Token expired!")

        refresh_payload = self.token_class(_validated_data["refresh"]).payload
        refresh_jti = refresh_payload["jti"]

        access_jti = self.token_class.access_token_class(_validated_data["access"]).payload["jti"]

        user_id = refresh_payload["user_id"]
        user = User.objects.get(id=user_id)
        self.authentication_service.save_session(user, access_jti, refresh_jti)
        
        return _validated_data