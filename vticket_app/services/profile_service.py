from typing import Union

from vticket_app.models.user import User
from vticket_app.serializers.user_serializer import UserSerializer

class ProfileService():
    def change_avatar(self, user_id: int, avatar_url: str) -> bool:
        try:
            instance = User.objects.get(id=user_id)
            instance.avatar_url = avatar_url
            instance.save(update_fields=["avatar_url"])
            
            return True
        except Exception as e:
            print(e)
            return False

    def get_profile_by_email(self, email: str) -> Union[dict | None]:
        try:
            instance = User.objects.get(email=email)
            return UserSerializer(instance, exclude=["password", "last_login"]).data
        except Exception as e:
            print(e)
            return None