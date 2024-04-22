import dataclasses
from vticket_app.models.user import User
from vticket_app.serializers.user_serializer import UserSerializer
from vticket_app.dtos.update_profile_dto import UpdateProfileDTO

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
        
    def change_profile(self, user_id: int, profile: UpdateProfileDTO) -> bool:
        try:
            instance = User.objects.get(id=user_id)
            _data = dataclasses.asdict(profile)
            user_serializer = UserSerializer(instance, data=_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return True
            else:
                print(user_serializer.errors)
                return False
        except Exception as e:
            print(e)
            return False