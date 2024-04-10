from vticket_app.models.user import User
from vticket_app.serializers.user_serializer import UserSerializer
from vticket_app.helpers.session_provider import SessionProvider

class AuthenticationService():
    account_serializer = UserSerializer
    session_provider = SessionProvider()

    def save_session(self, user: User, access_jti: str, refresh_jti: str):
        _session_data = self.account_serializer(user, many=False, exclude=["password"]).data
        self.session_provider.save_session(user.id, _session_data, access_jti, refresh_jti)
