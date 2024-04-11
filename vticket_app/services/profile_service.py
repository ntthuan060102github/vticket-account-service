from vticket_app.models.user import User
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