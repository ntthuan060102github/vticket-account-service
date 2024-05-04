from typing import Union

from vticket_app.models.user import User
from vticket_app.serializers.user_serializer import UserSerializer

class ProfileService():
    serializer_class = UserSerializer
    def change_avatar(self, user_id: int, avatar_url: str) -> bool:
        try:
            instance = User.objects.get(id=user_id)
            instance.avatar_url = avatar_url
            instance.save(update_fields=["avatar_url"])
            
            return True
        except Exception as e:
            print(e)
            return False
        
    def update_profile(self, user: User, update_data: dict) -> bool:
        try:
            print(user)
            for k, v in update_data.items():
                setattr(user, k, v)

            user.save(update_fields=update_data.keys())

            return True
        except Exception as e:
            print(e)
            return False
        
    def get_profile_by_id(self, user_id: int) -> User:
        try:
            return User.objects.get(id=user_id)
        except:
            return None

    def get_profile_by_email(self, email: str) -> Union[dict | None]:
        try:
            instance = User.objects.get(email=email)
            return UserSerializer(instance, exclude=["password", "last_login"]).data
        except Exception as e:
            print(e)
            return None

            