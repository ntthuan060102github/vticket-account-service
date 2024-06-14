from typing import Union

from vticket_app.models.user import User
from vticket_app.enums.account_status_enum import AccountStatusEnum
from vticket_app.serializers.user_serializer import UserSerializer
from django.db.models import Q

class UserService:
    def lock_user(self, user_id: int) -> 1 | 2 | 3:
        """
            Return value meaning:
            - 1: Account blocked, cann't execute block operation.
            - 2: Success.
            - 3: Failed.
        """

        try:
            user = User.objects.get(id=user_id)

            if user.status == AccountStatusEnum.BLOCKED:
                return 1
            
            user.status = AccountStatusEnum.BLOCKED
            user.save(update_fields=["status"])
            return 2
        except Exception as e:
            print(e)
            return 3

    def unlock_user(self, user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.status = AccountStatusEnum.ACTIVED
            user.save(update_fields=["status"])
            
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_user_by_id(self, user_id: int) -> Union[User | None]:
        try:
            user = User.objects.get(id=user_id)
            data = UserSerializer(user, exclude=["password"]).data
            
            return data
        except:
            return None
        
    def search(self, keyword: str|None) -> list:
        if keyword is None:
            queryset = self.all()
        else:
            queryset = User.objects.filter(
                Q(email__icontains=keyword) 
                | Q(first_name__icontains=keyword) 
                | Q(last_name__icontains=keyword)
            )

        return UserSerializer(queryset.order_by("id"), exclude=["password"], many=True).data
    
    def all(self) -> list[User]:
        return User.objects.all().order_by("id")
    
    def get_user_by_ids(self, ids: list):
        return User.objects.filter(id__in=ids)