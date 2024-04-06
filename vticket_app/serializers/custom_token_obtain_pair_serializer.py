from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from vticket_app.enums.account_status_enum import AccountStatusEnum

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        try:
            validated_data = super().validate(attrs)
        except AuthenticationFailed as e:
            if self.user.status in (AccountStatusEnum.UNVERIFIED, AccountStatusEnum.BLOCKED):
                raise PermissionDenied("non activated account!")
            raise e
        return validated_data